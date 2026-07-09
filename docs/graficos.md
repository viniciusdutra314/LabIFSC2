O LabIFSC2 precisa implementar algumas funções para converter um objeto `Medida` em um float, para que se possa criar gráficos em bibliotecas como o [Matplotlib](https://matplotlib.org/) e [Seaborn](https://seaborn.pydata.org/). Nesta seção, continuaremos o exemplo do campo magnético em função da distância da seção [Arrays](arrays.md).

## Nominais
Para obter os valores nominais de um array numpy de medidas, basta usar a função `nominais(array_medida, unidade)`:
```py
--8<-- "tests/test_doc_nominal.py:7:9"
```

## Incertezas
De maneira análoga, podemos também pegar as incertezas com `incertezas(array_medida, unidade)`:
```py
--8<-- "tests/test_doc_incerteza.py:7:9"
```

## Dispersão com barras de erro 
Eis um exemplo simples de como fazer um gráfico de dispersão com erros tanto em x quanto em y, basta usar a função do matplotlib `plt.errorbar`, `nominais` e `incertezas`. (Eu modifiquei as incertezas do exemplo para serem mais visíveis)

<img src="./images/graficos_scatter.jpg" width=400>

```py
--8<-- "tests/test_doc_grafico_scatter.py:5:22"
```

Repare que as unidades são variáveis no código que podem ser modificadas rapidamente.

## Curva Min/Max

As funções `curva_min` e `curva_max` são utilizadas para calcular a curva teórica considerando as incertezas nos parâmetros encontrados durante a regressão dos dados

Essas curvas são as [bandas de confiança](https://en.wikipedia.org/wiki/Confidence_and_prediction_bands) do fitting. Existem várias maneiras de fazê-las, mas basicamente estamos aproximando cada ponto amostrado como uma distribuição gaussiana e calculando o intervalo de confiança dessa gaussiana.

Resumidamente, estamos pegando \(2\sigma\) abaixo e acima do fitting. Pela hipótese de distribuição gaussiana[^1], os dados devem cair nesse intervalo com 95% de certeza.

Essas funções podem ser aplicadas diretamente em uma regressão,voltando para
o [exemplo da lei de kepler](regressão_prática.md#lei-de-potência), vemos que
o fitting tem pouca incerteza, visto que as curva min e max são bastante próximas

```py
--8<-- "tests/test_doc_kepler.py:82:85"
```

Essas funções também podem ser aplicadas diretamente em arrays de medidas
```py
--8<-- "tests/test_doc_curvaminmax_arrays.py:5:7"
```
Podemos alterar a quantidade de sigmas (por padrão são dois)
```py
--8<-- "tests/test_doc_curvaminmax_arrays.py:10:11"
```
## Curva teórica com erro
Regressões de dados inevitavelmente apresentam incertezas nos parâmetros encontrados. Podemos representá-las usando as funções `curva_min` e `curva_max`, que calculam a curva teórica \(\pm \, \, 2\sigma\).

<img src="./images/graficos_fitting.jpg" width=400>

```py
--8<-- "tests/test_doc_grafico_fitting.py:26:34"
```

Isso é algo pessoal, mas como as funções do matplotlib recebem vários argumentos
verbosos, eu recomendo usar um tipo de indentação chamada `Hanging indentation`, onde cada argumento ocupa uma linha de código. Assim, o código fica mais legível (na minha opinião) e menos horizontal.

[^1]:
    Se a biblioteca trabalha com distribuições estatísticas arbitrárias, por que fazer essa hipótese? Basicamente, cada chamada da função `intervalo_de_confianca` para uma distribuição arbitrária é \(O(n \log n)\) de complexidade, então calcular ela em centenas ou milhares de pontos é inviável.