Temos 4 regressões possíveis:

- `regressao_linear`(x_medidas,y_medidas)
- `regressao_polinomial`(x_medidas,y_medidas,grau)
- `regressao_exponencial`(x_medidas,y_medidas,base)
- `regressao_potencia`(x_medidas,y_medidas)

O resultado é guardado respectivamente em um objeto `MPolinomio`,`MExponencial` e `MPotencia`. Essas classes são
todas herdadas da mesma classe abstrata, então elas compartilham a mesma interface. Na prática essas classes
são irrelevantes, você provavelmente só vai pensar que está lidando com uma regressão.
## Calcular regressão

### Polinomial
Não há muito segredo nessa parte, as funções recebem os arrays de medidas em \(x\) e \(y\), é importante
salientar que essas funções recebem **Medidas**, isso porque queremos os parâmetros da regressão tento unidades.
Como exemplo, estamos imaginando aqui um objeto em queda livre vertical, 
nós registramos a sua posição na vertical em função de tempo e queremos encontrar a melhor parabola 
que se encaixa nos dados

```py
--8<-- "tests/test_doc_regressoes_construir.py:1:13"
```
Nós podemos acessar os coeficientes do polinômio fazendo, `polinomio.a`,`polinomio.b` etc (seguindo a convenção
de que **a** é o coeficiente de maior grau), ou fazendo a técnica de unpacking do python que nós igualamos os 
coeficientes ao polinomio (igual ao unpacking de uma tupla)

### Exponencial
!!! warning
    Lembre-se que, para regressões  exponenciais, todos os valores de y precisam ser positivos. No caso da regressão de lei de potência, os valores em x também precisam ser positivos. Além disso, um valor pode não ser negativo, mas devido à incerteza associada, ele pode assumir valores negativos

Imagine um experimento que queiramos determinar a meia vida de um material radioativo, *as escalas de massa e tempo
são somente ilustrativas*, podemos acessar a constante multiplicativa fazendo `exponencial.cte_multiplicativa` e o expoente
fazendo `exponencial.expoente`.

```py
--8<-- "tests/test_doc_regressoes_construir.py:13:24"
```
Repare que a regressão aceita uma base (por padrão base=\(e\))

## Amostrar

Quando queremos fazer o gráfico de uma curva precisamos amostrar essa curva em conjunto de pontos,
tomemos o exemplo simples de fazer o gráfico da função exponencial

```py
--8<-- "tests/test_doc_grafico_seno.py:1:6"
```

<img src="./images/exponencial.jpg" width=300>

A interface do LabIFSC2 é parecida, a diferença é que devido a [propagação de erros](propagacao_de_erros.md) ser feita por monte carlo, além da curva temos também a dispersão dessa curva teórica.

- `amostrar(intervalo_em_x,unidade_y)`

### curvamin e curvamax


### Exemplos