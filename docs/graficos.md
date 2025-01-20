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

```py
--8<-- "tests/test_doc_grafico_scatter.py:1:16"
```

Repare que as unidade são variáveis no código que podem ser modificadas rapidamente, o resultado é esse:
<img src="exemplo.jpg" width=400>

##  