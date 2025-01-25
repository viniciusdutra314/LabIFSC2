Temos 4 regressões possíveis:

- `regressao_linear`(x_medidas,y_medidas)
- `regressao_polinomial`(x_medidas,y_medidas,grau)
- `regressao_exponencial`(x_medidas,y_medidas,base)
- `regressao_potencia`(x_medidas,y_medidas)

O resultado é guardado respectivamente em um objeto `MPolinomio`,`MExponencial` e `MPotencia`. Essas classes são
todas herdadas da mesma classe abstrata, então elas compartilham a mesma interface. Na prática essas classes
são irrelevantes, você provavelmente só vai pensar que está lidando com uma regressão.
!!! warning
    Lembre-se que, para regressões  exponenciais, todos os valores de y precisam ser positivos. No caso da regressão de lei de potência, os valores em x também precisam ser positivos. Além disso, um valor pode não ser negativo, mas devido à incerteza associada, ele pode assumir valores negativos

## Calcular regressão

### Polinomial
Não há muito segredo nessa parte, as funções recebem os arrays de medidas em \(x\) e \(y\), é importante
salientar que essas funções recebem **Medidas**, isso porque queremos os parâmetros da regressão tento unidades.
Como exemplo, estamos imaginando aqui um objeto em queda livre vertical, 
nós registramos a sua posição na vertical em função de tempo e queremos encontrar a melhor parabola 
que se encaixa nos dados

```py
--8<-- "tests/test_doc_regressoes_construir.py:7:16"
```
Nós podemos acessar os coeficientes do polinômio fazendo, `polinomio.a`,`polinomio.b` etc (seguindo a convenção
de que **a** é o coeficiente de maior grau), ou fazendo a técnica de unpacking do python que nós igualamos os 
coeficientes ao polinomio (igual ao unpacking de uma tupla)

### Exponencial

Imagine um experimento que queiramos determinar a meia vida de um material radioativo, *as escalas de massa e tempo
são somente ilustrativas*, podemos acessar a constante multiplicativa fazendo `exponencial.cte_multiplicativa` e o expoente
fazendo `exponencial.expoente`.

```py
--8<-- "tests/test_doc_regressoes_construir.py:23:33"
```
Repare que a regressão aceita uma base (por padrão base=\(e\))

## Lei de Potência
Um exemplo clássico da lei de potência é a terceira lei de Kepler, onde o período orbital (T) se relaciona com o raio orbital (R) segundo:
$$\frac{T²}{R³}=\frac{4\pi^2}{GM}\to T \propto R^{1.5}$$
A regressão de lei de potência encontra parâmetros como a constante multiplicativa e o expoente  a partir de dados experimentais. O exemplo abaixo pega dados da [NASA](https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_british.html)
para demonstrar experimentalmente a terceira lei de Kepler, eu peguei as distâncias em milhas justamente para demonstrar
como com o LabIFSC2 você não precisa se preocupar com unidades.


```py
--8<-- "tests/test_doc_kepler.py:8:29"
```
Perceba como essa lei de fato aproxima muito bem os dados, essa 'lei' na verdade é uma aproximação que só considera
a atração gravitacional do sol, então é esperado observar alguns pequenos desvios visto que o sistema solar não é composto
só pelo sol, mas um sistema complexo de dezenas de milhares de corpos massivos.
## Amostrar

Quando queremos fazer o gráfico de uma curva precisamos amostrar essa curva em conjunto de pontos, para isso
precisamos especificar em que intervalo queremos calcular a curva e em que unidades esse cálculo deve retornar

- `amostrar(intervalo_em_x,unidade_y)`

No exemplo abaixo calculamos o que a nossa regressão (da secção anterior) no intervalo dos planetas do sistema solar ([0,30] unidades astronômicas),
e pedimos para ele retornar esse resultado em anos

```py hl_lines="36 61"
--8<-- "tests/test_doc_kepler.py:36:63"
```

<img src="./images/kepler.jpg" width=600>

Podemos visualizar esses dados fazendo um pequeno código em matplotlib, para ler mais sobre 
gráficos vá para a secção [Gráficos](graficos.md)

```py 
--8<-- "tests/test_doc_kepler.py:64:79"
```


!!!warning
    Visto que a biblioteca realiza uma simulação Monte Carlo para cada ponto da curva, usar
    muitos pontos de amostragem provavelmente irá causar uma lentidão no seu código, no meu
    notebook eu tive uma boa experiência amostrando a regressão em **100 pontos**, recomendo você
    começar com esse valor, se a curva ficar pouco definida aumente esse valor.

    Outra dica, caso tenha que usar a amostragem mais de uma vez, salve o array em uma variável,
    assim não ira precisar calcular duas vezes. Eu fiz isso no código de exemplo, eu queria printar
    a amostragem e também usa-la no matplotlib, isso é uma dica geral de programação, tente sempre
    calcular as coisas só uma vez.


## curva_min e curva_max
Como estamos tratando os fittings usando medidas, também temos a incerteza associada ao fitting,
quando chamamos a função `amostrar`, a biblioteca automaticamente cria dois atributos no objeto
regressão, `regressao.curva_min` e `regressao.curva_max`.

Essas curvas são as [bandas de confiança](https://en.wikipedia.org/wiki/Confidence_and_prediction_bands) do fitting, existem
várias maneiras de faze-las mas basicamente estamos aproximando cada ponto amostrado como uma distribuição gaussiana e
calculando o intervalo de confiança dessa gaussiana.

Resumidamente, estamos pegando \(2\sigma\) abaixo e acima do fitting, pela hipótese da distribuição gaussiana[^1],
os dados devem cair nesse intervalo com 95% de certeza

Caso você queira uma confiança diferente dessa basta chamar a função `regressao.mudar_intervalo_de_confianca`
e especificar quantos sigmas de confiança

[^1]:
    Se a biblioteca trabalha com distribuições estatísticas arbitrárias, por que fazer essa hipótese?
    Basicamente cada chamada da função intervalo_de_confiança para uma distribuição arbitrária, 
    é \(O(nln(n))\) de complexidade, então calcular ela em centenas ou milhares de pontos é inviável