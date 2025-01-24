!!! warning
    Mesmo que as funções de regressão da biblioteca recebam Medidas, a regressão é feita **sem considerar as
    incertezas nas medições**, é passado arrays de Medidas somente para a conversão de unidades ser feita.
    Para os erros serem considerados teríamos que usar algum método de [Total least square](https://en.wikipedia.org/wiki/Total_least_squares) que envolveria escolher alguma função peso para cada medida, o que faria as regressões
    serem mais corretas porém incompatíveis com a apostila


# Regressão Linear

Quando temos uma equação física que prevê a relação entre duas ou mais variáveis, geralmente tentamos encontrar a  curva teórica prevista pela equação que mais se encaixe com os dados experimentais. Um exemplo é a lei de Hooke:

$$\vec{F}=-k\vec{x}$$

Para certos regimes de deslocamento, a força aplicada a uma mola é linear com a sua distensão. Vamos imaginar que um experimento foi realizado e chegamos a este conjunto de forças e deslocamentos.

```py
--8<-- "tests/test_doc_lei_de_hook.py:9:10"
```

Qual é a constante elástica \(k\) da mola?

Na prática, a relação não é totalmente linear entre os dados, então precisamos criar algum tipo de critério para determinar qual reta é "melhor" do que outra. Um critério muito utilizado é a minimização dos quadrados dos desvios[^1], chamemos de \(S\):

$$S=\sum (y_{real}-y_{teórico})^2 = \sum (y_{real}-ax-b)^2$$

Para encontrar esse mínimo, podemos pensar no desvio como sendo uma função da nossa curva teórica \(S(a,b)\). Existe um conjunto de coeficientes angular e linear que minimiza essa função. Nesse ponto, temos[^2]:

$$\frac{\partial S}{\partial a} = \frac{\partial S}{\partial b} = 0$$

Comecemos com a equação do coeficiente linear:

$$\frac{\partial}{\partial b} \left(\sum (y_{real}-ax-b)^2\right) = -2\sum (y_{real}-ax-b) = 0 \rightarrow a\overline{x} + b = \sum y_{real}$$

Podemos fazer um raciocínio análogo para o coeficiente angular:

$$\frac{\partial}{\partial a} \left(\sum (y_{real}-ax-b)^2\right) = -2\sum (y_{real}-ax-b)x = 0$$

Que pode ser rearranjado como:

$$a\sum x^2 + b\sum x = \sum xy_{real}$$

Perceba que temos um **sistema linear em \(a\) e \(b\)**:

$$a\sum x^2 + b\sum x = \sum xy_{real}$$
$$a\overline{x} + b = \sum y_{real}$$

Como \(x\) e \(y\) são conhecidos, podemos inverter a matriz desse sistema linear e achar \(a\) e \(b\). Esta é uma demonstração das fórmulas do livro.

# Regressão Polinomial

O método descrito acima de tomar derivadas da função e chegar a um sistema de \(N\) variáveis se estende para polinômios de grau arbitrário. **Mas como um sistema linear pode achar coeficientes de uma parábola?**

O desvio seria \(S=\sum (y-ax^2-bx-c)^2\), faríamos então:

$$\frac{\partial S}{\partial a} = \frac{\partial S}{\partial b} = \frac{\partial S}{\partial c}= 0$$


A grande sacada é perceber que as equações são lineares nos coeficientes e não em \(x\). Claramente, uma regressão de uma parábola terá termos quadráticos em \(x\), mas as equações da minimização são lineares em \(a\), \(b\) e \(c\). 



No fim, você chegará a uma equação matricial que te dá os coeficientes do polinômio para qualquer grau \(N\)[^3]:

$$\text{coeficientes} = (A^T A)^{-1} A^T y$$

Em que a matriz A é matrix de [Vandermonde](https://en.wikipedia.org/wiki/Vandermonde_matrix), definida como \(A_{ij}=x^j_i\)
É interessante pensar que você, em teoria, pode fazer o método dos mínimos quadrados para um polinômio arbitrário com uma linha de Python.

Caso queiram ver mais sobre, recomendo este [artigo](https://www.researchgate.net/publication/337103890_Linear_Least_Squares_Versatile_Curve_and_Surface_Fitting_CDT-17) do Luciano da Fontoura Costa. Ele é um pesquisador do IFSC que, além dos seus artigos de pesquisa, também publica vários materiais interessantes a nível de graduação chamados de CDT (Costa’s Didactic Texts).

# Regressão Exponencial

Também podemos usar o mesmo método para o caso exponencial, aplicando um truque simples:

$$y = Ae^{kx}$$
$$\text{Tomando log dos dois lados}$$
$$\ln(y) = kx + \ln(A)$$

Que é uma equação linear se plotarmos \(x \times \ln(y)\). Talvez seja difícil ver que isso é realmente uma reta. Minha sugestão é esquecer totalmente a variável \(y\) original e pensar que existe uma nova variável chamada \(Y\) que se conecta com \(y\). Assim, \(Y = \ln(y)\). Como \(\ln(A)\) é uma constante, vamos dar um novo nome, por que não \(B = \ln(A)\)? Reescrevendo a equação:

$$Y = kx + B$$

Agora creio que seja fácil ver que é de fato linear a menos de uma transformação de variável.

## Regressão Lei de Potência

Uma lei de potência segue o mesmo truque:

$$y = Ax^n$$
$$\text{Tomando log dos dois lados}$$
$$\ln(y) = n\ln(x) + \ln(A)$$

Se fizermos um gráfico \(\ln(y) \times \ln(x)\), teremos uma reta.

[^1]: Sim, existem outros critérios. A minimização do módulo dos desvios também é válida (e em alguns casos até melhor do que o método dos mínimos quadrados), mas os mínimos quadrados têm a vantagem de ter uma solução analítica fechada usando apenas o ferramental básico de Cálculo I e Álgebra Linear, então certamente tem um apelo maior para a graduação.

[^2]: Mas você só provou que um extremo da função ocorre em \(a\) e \(b\), não que seja um mínimo! Bem, existe um passo geralmente omitido que seria a análise de que a função \(S\) é quadrática em \(a\) e \(b\), ela é **convexa**! Um dos teoremas mais fortes e úteis de otimização de funções convexas é que o extremo local é o extremo global. Pela convexidade, se provamos que é um extremo, então ou é um mínimo ou é um máximo. Claramente não é um máximo. Informalmente, podemos pensar que é sempre possível achar uma reta pior.

[^3]: Essa fórmula jogada não significa muita coisa, mas o interessante é que os mínimos quadrados possuem uma interpretação geométrica bem legal. Se o polinômio passasse por todos os pontos, teríamos um sistema linear \(A\vec{x} = \vec{b}\), mas não temos isso. Na verdade, temos \(A\vec{x} \approx \vec{b}\). Os mínimos quadrados são equivalentes a minimizar \(||A\vec{x} - \vec{b}||^2\). Estamos minimizando a norma da distância entre os vetores, fazendo a projeção ortogonal de um no outro. Esse vetor pode ser encontrado aplicando a pseudo-inversa de Penrose (sim, o mesmo Penrose do Nobel de 2020). Ela não é exatamente uma inversa porque não estamos resolvendo o sistema exatamente, mas sim, estamos atrás do vetor que está mais "próximo" da solução.