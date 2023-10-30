Regressão polinomial usando o método dos [mínimos quadrados](https://www.researchgate.net/publication/337103890_Linear_Least_Squares_Versatile_Curve_and_Surface_Fitting_CDT-17), o código é escrito usando a função 
`polyfit` do numpy, a sua grande vantagem é que são aceitas Medidas nos arrays \(x\) e \(y\).

É retornado os coeficientes do polinômio como Medidas com seus erros estimados, um detalhe é que 
os coeficientes são ordenados com **grau crescente (\(c+bx+ax^2\) e não \(ax^2+bx+c\) )**


```{.py3 title="Exemplo de 2º grau"}
    x_dados=np.array([1, 2, 3, 4])
    y_dados=np.array([1.9 , 3.1 , 5.85 , 10.9])
    c,b,a= regressao_polinomial(x_dados,y_dados,grau=2) 
    #c=(2.8±0.4) b=(-1.8 ±0.4) a=(0.96 ±0.08)

```

## Retornar função
Para criação de gráficos, às vezes é mais prático a `regressao_polinomial` retornar
um polinomio do que os coeficientes, com o parametro extra `func=True` isso
é possível. É retornado um [MPolinomio](../MPolinomio/Introdução.md) que atua como função

```{.py3 linenums=1 hl_lines=3}
    x_dados=np.array([1, 2, 3, 4])
    y_dados=np.array([1.9 , 3.1 , 5.85 , 10.9])
    parabola= regressao_polinomial(x_dados,y_dados,grau=2,func=True) 
    x=np.linspace(1,4,100)
    y=parabola(x)
```

o [MPolinomio](../MPolinomio/Introdução.md) quando calculado nos valores de x,
irá retornar um array de Medidas que junto com os métodos [CurvaMin](../Arrays/Incertezas.md) e 
[CurvaMax](../Arrays/CurvaMinMax.md) é possível criar facilmente um gráfico com o erro
estimado do polinômio

```{.py3 linenums=6}
    import matplotlib.pyplot as plt
    plt.scatter(x_dados,y_dados)
    plt.plot(x,y,color='r')
    plt.fill_between(x,CurvaMin(y),CurvaMax(y),alpha=0.5)
```
![Image](regressao_polinomial.jpg)
