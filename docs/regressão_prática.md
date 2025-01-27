## Tipos de regressão

Temos 4 tipos de regressões possíveis:

- `regressao_linear(x_medidas, y_medidas)`
- `regressao_polinomial(x_medidas, y_medidas, grau)`
- `regressao_exponencial(x_medidas, y_medidas, base)`
- `regressao_potencia(x_medidas, y_medidas)`

O resultado é armazenado respectivamente em um objeto `MPolinomio`, `MExponencial` e `MPotencia`. Essas classes são todas herdadas de uma mesma classe abstrata, então elas compartilham a mesma interface. Na prática, essas classes são irrelevantes, você provavelmente só vai pensar que está lidando com uma regressão.

!!! warning
    Lembre-se que, para regressões exponenciais, todos os valores de y precisam ser positivos. No caso da regressão de lei de potência, os valores de x também precisam ser positivos. Além disso, um valor pode não ser negativo, mas devido à incerteza associada, ele pode assumir valores negativos.

## Calcular Regressão

### Polinomial
Não há muito segredo nessa parte, as funções recebem os arrays de medidas em \(x\) e \(y\). É importante salientar que essas funções recebem **Medidas**, isso porque queremos os parâmetros da regressão tendo unidades. Como exemplo, estamos imaginando aqui um objeto em queda livre vertical, nós registramos a sua posição na vertical em função do tempo e queremos encontrar a melhor parábola que se encaixa nos dados.

```py
--8<-- "tests/test_doc_regressoes_construir.py:7:16"
```
Nós podemos acessar os coeficientes do polinômio fazendo `polinomio.a`, `polinomio.b` etc. (seguindo a convenção de que **a** é o coeficiente de maior grau), ou utilizando a técnica de unpacking do Python, igualando os coeficientes ao polinômio (igual ao unpacking de uma tupla).

### Exponencial

Imagine um experimento em que queremos determinar a meia-vida de um material radioativo. *As escalas de massa e tempo são somente ilustrativas*. Podemos acessar a constante multiplicativa fazendo `exponencial.cte_multiplicativa` e o expoente fazendo `exponencial.expoente`.

```py
--8<-- "tests/test_doc_regressoes_construir.py:23:33"
```
Repare que a regressão aceita uma base (por padrão base=\(e\)).

## Lei de Potência
Um exemplo clássico de lei de potência é a terceira lei de Kepler, onde o período orbital (T) se relaciona com o raio orbital (R) segundo:
$$\frac{T²}{R³}=\frac{4\pi^2}{GM}\to T \propto R^{1.5}$$
A regressão de lei de potência encontra parâmetros como a constante multiplicativa e o expoente a partir de dados experimentais. O exemplo abaixo pega dados da [NASA](https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_british.html) para demonstrar experimentalmente a terceira lei de Kepler. Eu peguei as distâncias em milhas justamente para demonstrar como com o LabIFSC2 você não precisa se preocupar com unidades.

```py
--8<-- "tests/test_doc_kepler.py:8:30"
```
Perceba como essa lei de fato aproxima muito bem os dados. Essa 'lei' na verdade é uma aproximação que só considera a atração gravitacional do sol, então é esperado observar alguns pequenos desvios visto que o sistema solar não é composto só pelo sol, mas um sistema complexo de dezenas de milhares de corpos massivos.

## Amostrar

Quando queremos fazer o gráfico de uma curva, precisamos amostrar essa curva em um conjunto de pontos. Para isso, precisamos especificar em que intervalo queremos calcular a curva e em que unidades esse cálculo deve retornar.

- `amostrar(intervalo_em_x, unidade_y)`

No exemplo abaixo, calculamos a nossa regressão (da seção anterior) no intervalo de distâncias dos planetas do sistema solar ([0,30] unidades astronômicas), e pedimos para ele retornar esse resultado em anos.

```py hl_lines="36 61"
--8<-- "tests/test_doc_kepler.py:36:63"
```

<img src="./images/kepler.jpg" width=600>

Podemos visualizar esses dados fazendo um pequeno código em matplotlib. Para ler mais sobre gráficos, vá para a seção [Gráficos](graficos.md).

```py 
--8<-- "tests/test_doc_kepler.py:64:79"
```

!!! warning
    Visto que a biblioteca realiza uma simulação Monte Carlo para cada ponto da curva, usar muitos pontos de amostragem provavelmente irá causar uma lentidão no seu código. No meu notebook, eu tive uma boa experiência amostrando a regressão em **100 pontos**. Recomendo você começar com esse valor, se a curva ficar pouco definida, aumente esse valor.

    Outra dica: caso tenha que usar a amostragem mais de uma vez, salve o array em uma variável, assim não irá precisar calcular duas vezes. Eu fiz isso no código de exemplo, eu queria printar a amostragem e também usá-la no matplotlib. Isso é uma dica geral de programação, tente sempre calcular as coisas só uma vez.

## curva_min e curva_max

Uma função que creio ser muito útil é aplicar `curva_min` e `curva_max` em uma regressão. Para que tudo sobre gráficos fique na sua respectiva seção, vá para a seção de [gráficos](graficos.md#curva-minmax) para ler a documentação sobre isso.

