O LabIFSC2 precisa implementar algumas funções para converter um objeto `Medida` em um 
float, para que se possa criar gráficos em bibliotecas como o [Matplotlib](https://atplotlib.org/)/[Seaborn](https://seaborn.pydata.org/). Nessa secção continuaremos o exemplo do campo magnético em função da distância da secção [Arrays](arrays.md)

## Nominais
Para obter os valores nominais de um array numpy de medidas basta usar a função `nominais(array_medida,unidade)`
```py
--8<-- "tests/test_doc_nominal.py:1:5"
```


## Incertezas
De maneira análogo podemos também pegar as incertezas com `incertezas(array_medida,unidade)`
```py
--8<-- "tests/test_doc_incerteza.py:1:5"
```

## Dispersão com barras de erro 
Eis um exemplo simples de como fazer um gráfico de dispersão com erros tanto em x quanto em y,
basta usar a função do matplotlib [`plt.errorbar`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.errorbar.html), `nominais` e `incertezas`.


<img src="./images/graficos_scatter.jpg" width=400>

```py hl_lines="12-16"
--8<-- "tests/test_doc_grafico_scatter.py:1:19"
```

Repare que as unidade são variáveis no código que podem ser modificadas rapidamente.



## Curva Min/Max

As funções `curva_min` e `curva_max` são utilizadas para calcular a curva teórica considerando as incertezas nos parâmetros encontrados durante a regressão dos dados (chamados de [Confidence and prediction bands]([Confidence and prediction bands)](https://en.wikipedia.org/wiki/Confidence_and_prediction_bands))

##  Curva teórica com erro
Regressões de dados inevitavelmente apresentam incertezas nos parâmetros encontrados, podemos representa-las usando as funções `curva_min` e `curva_max` que calculam a curva teórica \(\pm \, \, 2\sigma \)

<img src="./images/graficos_fitting.jpg" width=400>

```py hl_lines="20-29"
--8<-- "tests/test_doc_grafico_fitting.py:1:30"
```

Perceba que para lidar com as unidades acaba que a sintaxe fica infelizmente verbosa, isso é algo pessoal mas nesse caso eu recomendo usar um tipo de indentação chamada `Hanging indentation ` em cada argumento ocupa uma linha de código, assim o código fica mais legível (na minha opinião) e menos horizontal.

