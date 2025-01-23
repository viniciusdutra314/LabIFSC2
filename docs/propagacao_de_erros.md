!!! warning
    A leitura dessa parte da documentação não é obrigatória para o uso da biblioteca, caso sinta que a matemática/estatística é muito complexa, sinta-se livre para pular. Mas caso queira realmente entender como as coisas funcionam por baixo dos panos essa secção é pra você.




Nesta seção, explicarei em mais detalhes como a biblioteca propaga incertezas, o método usado é mais geral, mas ainda assim compatível com o da apostila. Nos testes unitários da biblioteca, comparamos os erros calculados pelo LabIFSC2 com as bibliotecas [uncertainties](https://pythonhosted.org/uncertainties/) e [LabIFSC](https://github.com/gjvnq/LabIFSC), chegando a um acordo geralmente de \(10^{-3}\) para erros pequenos, onde os métodos devem ser equivalentes.

## Apostila
A apostila se baseia principalmente no GUM (Guide to the Expression of Uncertainty in Measurement)[^1]. O método é uma propagação linear baseada em uma série de Taylor.

Começamos com uma série de Taylor de uma função de \(N\) variáveis, ou seja, uma boa aproximação para **pequenas variações da função**:

$$f(\mathbf{x}+\Delta \mathbf{x})\approx f(\mathbf{x})+\sum_{i} \frac{\partial f}{\partial x_{i}}\Delta x_{i}$$

$$(f(\mathbf{x}+\Delta \mathbf{x})-f(\mathbf{x}))²\approx (\sum_{i} \frac{\partial f}{\partial x_{i}}\Delta x_{i})²$$

Note que o lado esquerdo nada mais é que a variação da função \(\Delta f\). Se pegarmos o valor esperado, teremos a variância de \(f\) (\(\sigma²_{f}\)):

$$\mathbb{E}[(f(\mathbf{x}+\Delta \mathbf{x})-f(\mathbf{x}))²]\approx \mathbb{E}[(\sum_{i} \frac{\partial f}{\partial x_{i}}\Delta x_{i})²]$$

Supondo que \(\Delta x_i\) tenha uma distribuição simétrica \(\mathbb{E}(\Delta x_{i})=0\), os termos cruzados \(\mathbb{E}(\Delta x_{i}\Delta x_{j})=\mathbb{E}(\Delta x_{i})\mathbb{E}(\Delta x_{j})=0\) desaparecem (se supormos que são totalmente independentes).

Logo:

$$\sigma²_{f}=\sum_{i} \left(\frac{\partial f}{\partial x_{i}}\sigma_{x_{i}}\right)²$$

Se quisermos em termos do desvio padrão e não da variância, temos:

$$\sigma_{f}=\sqrt{\sum_{i} \left(\frac{\partial f}{\partial x_{i}}\sigma_{x_{i}}\right)²}$$

Essa é essencialmente a fórmula usada na apostila. Para o caso de uma variável, se reduz a \(\sigma_{f}=|\frac{\partial f}{\partial x}\sigma_{x}|\). A diferença é que a apostila ignora a raiz quadrada na expressão de incertezas com mais de uma variável, superestimando assim o erro.

Pensando intuitivamente, erros não podem simplesmente se somar, visto que, pela sua natureza aleatória, é esperado que existam erros que acabem "compensando" outros.

## Monte Carlo
Imagine que temos uma medida indireta \(y\) que depende de um conjunto de \(N\) medidas:

$$y=f(x_1,x_2,\dots,x_n)$$

Cada variável \(x_i\) tem sua PDF ([probability density function](https://en.wikipedia.org/wiki/Probability_density_function)), que é uma forma matemática de dizer que não temos certeza sobre seus valores. Por simplicidade, assumimos que medidas diretas têm distribuições gaussianas (centradas em uma média \(\mu\) e uma variância \(\sigma²\)).

O Método Monte Carlo consiste em simular diversas medidas experimentais no computador (usando um gerador de números aleatórios com as respectivas PDFs). Dessa forma, geramos um histograma de possíveis valores de \(y\); esse histograma é a PDF de \(y\).

O interessante desse método é que o histograma de \(y\) não necessariamente é analítico (geralmente com formatos bem estranhos para incertezas grandes). Esse histograma é utilizado para diversas coisas na biblioteca:

- Ser usado como PDF para outra propagação de incerteza
- Cálculo do intervalo de confiança
- A média e o desvio padrão da PDF são usados no `print(medida)`

### Exemplo com a gravidade
Retornando ao exemplo da estimativa da gravidade usando um pêndulo, mas agora com incertezas maiores em \(T\) e \(L\) (para que os efeitos fiquem mais visíveis).

A classe `Medida` possui um atributo chamado `histograma`, onde estão guardados os histogramas. No dia a dia, esse atributo deve ser raramente acessado, mas para fins didáticos ele é interessante.

```py 
--8<-- "tests/test_doc_gravidade_histograma.py:8:15"
```

Repare como \(T\) e \(L\) são gaussianas (\(\mu_L=15cm\), \(\sigma_L=1cm\)) e (\(\mu_T=780ms\), \(\sigma_T=80ms\)).

<img src="./images/gravidade_histograma.jpg" width=600>

Já o histograma de \(g\) é centralizado em \(10m/s²\), mas observe que ele possui uma cauda para a direita. A distribuição não é simétrica, logo, não é gaussiana. Se usássemos \(g\) para outros cálculos, esse desvio de uma gaussiana provavelmente iria se amplificando. Esse fato não é observado no método GUM, que assume linearidade e basicamente tudo é uma gaussiana.


!!! tip
    Por padrão a biblioteca utiliza \(N=10^5\) amostras, acredito que esse seja um número que vá satisfazer a maioria das aplicações e não trazer problemas de performance para a biblioteca, mas caso queira alterar esse número é só usar
    `alterar_monte_carlo_sample`, por enquanto Medidas com N diferentes não se interagem corretamente (pense o que isso significa), então se quiser mudar esse número é recomendado alterar no começo do código ou as varíaveis usadas só terem escopo dentro dessa alteração do N




[^1]: O método GUM é amplamente utilizado em metrologia e calibragem de equipamentos. Existem diversas referências para quem quiser aprender mais. Eu, pessoalmente, achei um material introdutório e interessante em:
    
    Kirkup, L., Frenkel, R. B. (2006). An Introduction to Uncertainty in Measurement: Using the GUM (Guide to the Expression of Uncertainty in Measurement). Reino Unido: Cambridge University Press.

[^2]: O principal material usado na implementação do Monte Carlo foi o próprio material suplementar do GUM sobre Monte Carlo. É interessante notar que esse material explicitamente considera o método Monte Carlo como uma forma mais precisa de calcular incertezas:

    “Evaluation of Measurement Data — Supplement 1 to the ‘Guide to the Expression of Uncertainty in Measurement’ — Propagation of Distributions Using a Monte Carlo Method,” 2008. https://doi.org/10.59161/JCGM101-2008.