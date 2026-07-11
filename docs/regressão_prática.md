## Tipos de regressão

Temos 4 tipos de regressões possíveis:

- `regressao_linear(x_medidas, y_medidas)`
- `regressao_polinomial(x_medidas, y_medidas, grau)`
- `regressao_exponencial(x_medidas, y_medidas, base)`
- `regressao_potencia(x_medidas, y_medidas, x0=None)`

O resultado das regressões linear e polinomial é armazenado em um objeto `AjustePolinomial`. Para as regressões exponencial e de lei de potência, os resultados são armazenados em `AjusteExponencial` e `AjusteLeiDePotencia`, respectivamente. Esses objetos são chamáveis e agem como funções para avaliar o ajuste em novos pontos. Na prática, você só precisará chamá-los passando suas variáveis independentes.

!!! warning
    Lembre-se que, para regressões exponenciais, todos os valores de y precisam ser positivos. No caso da regressão de lei de potência, os valores de x também precisam ser positivos. Além disso, um valor pode não ser negativo, mas devido à incerteza associada, ele pode assumir valores negativos.

## Calcular Regressão

### Polinomial
A função `regressao_linear` é um caso especial da **`regressao_polinomial`** (com grau=1), criada somente por conveniência.


Não há muito segredo nessa parte, as funções recebem os arrays de medidas em \(x\) e \(y\). É importante salientar que essas funções recebem **Medidas**, isso porque queremos os parâmetros da regressão tendo unidades. Como exemplo, estamos imaginando aqui um objeto em queda livre vertical, nós registramos a sua posição na vertical em função do tempo e queremos encontrar a melhor parábola que se encaixa nos dados.

```py
--8<-- "tests/doctest/test_doc_regressoes_construir.py:regressao_polinomial"
```
Nós podemos acessar os coeficientes utilizando a técnica de unpacking do Python, igualando os coeficientes ao ajuste/polinômio (igual ao unpacking de uma tupla, retornando em ordem decrescente de grau: do termo de maior grau até o termo constante).

### Exponencial

Imagine um experimento em que queremos determinar a meia-vida de um material radioativo. *As escalas de massa e tempo são somente ilustrativas*. Podemos acessar a amplitude do ajuste fazendo `exponencial.amplitude` e o expoente fazendo `exponencial.expoente`.

```py
--8<-- "tests/doctest/test_doc_regressoes_construir.py:regressao_exponencial"
```
Repare que a regressão aceita uma base (por padrão base=\(e\)).

## Lei de Potência
Um exemplo clássico de lei de potência é a terceira lei de Kepler, onde o período orbital (T) se relaciona com o raio orbital (R) segundo:
$$\frac{T²}{R³}=\frac{4\pi^2}{GM}\to T \propto R^{1.5}$$
A regressão de lei de potência encontra a amplitude e potência a partir de dados experimentais da forma:
$$y = \text{amplitude} \cdot \left(\frac{x}{x_0}\right)^{\text{potência}}$$

É usado aqui um valor de referência \(x_0\) por uma razão técnica, ele garante que a razão \(\frac{x}{x_0}\) seja adimensional, prevenindo que a amplitude receba tenha uma unidade com expoentes fracionários (como \(\text{s/m}^{1.4853}\)), que faz com ela seja uma `Medida` quase que impossível de interagir e ser comparada com outra `Medida`. Usando \( x_0 \), garantimos que a amplitude tem exatamente a mesma unidade física da variável \(y\).

O exemplo abaixo pega dados da NASA para demonstrar experimentalmente a terceira lei de Kepler. Eu peguei as distâncias em milhas justamente para demonstrar como que com o LabIFSC2 você não precisa se preocupar com unidades.

```py
--8<-- "tests/doctest/test_doc_kepler.py:kepler_regressao"
```
Perceba como essa lei de fato aproxima muito bem os dados. Essa 'lei' na verdade é uma aproximação que só considera a atração gravitacional do sol, então é esperado observar alguns pequenos desvios visto que o sistema solar não é composto só pelo sol, mas um sistema complexo de dezenas de milhares de corpos massivos.

## Avaliar / Amostrar

Para avaliar um ajuste em um conjunto de pontos, basta chamá-lo como uma função. O objeto do ajuste receberá uma `Medida` ou uma sequência de `Medida` e retornará o resultado calculado com propagação de incerteza correspondente. Para obter os valores numéricos em uma unidade específica (por exemplo, para plotar com o matplotlib), use as funções `nominais` e `incertezas`.

- `ajuste(x)` -> Retorna o(s) valor(es) ajustado(s) como `Medida` ou array de `Medida`.


No exemplo abaixo, calculamos a nossa regressão (da seção anterior) no intervalo de distâncias dos planetas do sistema solar ([0,30] unidades astronômicas), e pedimos para ele retornar esse resultado em anos.

```py
--8<-- "tests/doctest/test_doc_kepler.py:kepler_amostragem"
```

<img src="./images/kepler.jpg" width=600>

Podemos visualizar esses dados fazendo um pequeno código em matplotlib. Para ler mais sobre gráficos, vá para a seção [Gráficos](graficos.md).

```py 
--8<-- "tests/doctest/test_doc_kepler.py:kepler_grafico"
```

!!! warning
    Visto que as operações matemáticas com `Medida` realizam simulação Monte Carlo por baixo dos panos, avaliar a regressão em muitos pontos de amostragem pode causar uma lentidão no seu código. Uma boa prática é avaliar a regressão em cerca de **100 pontos**. Recomendo começar com esse valor.

    Outra dica: caso tenha que usar a amostragem mais de uma vez, salve o array em uma variável, assim não precisará calcular duas vezes. Eu fiz isso no código de exemplo, salvando o resultado de `fitting(x)` em uma variável.

## curva_min e curva_max

Uma função que creio ser muito útil é aplicar `curva_min` e `curva_max` em uma regressão. Para que tudo sobre gráficos fique na sua respectiva seção, vá para a seção de [gráficos](graficos.md#curva-minmax) para ler a documentação sobre isso.
