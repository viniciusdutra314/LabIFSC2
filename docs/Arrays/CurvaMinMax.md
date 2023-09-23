As funções `CurvaMin` e `CurvaMax` são usadas na criação de gráficos com propagação de erro em curvas, elas recebem um array de Medidas e retornam um array com a curva máximo/mínima,abaixo consta um gráfico de uma queda livre usando Matplotlib e utilizando a gravidade com valor (9.5 ± 0.5)m/s2 . 

```{.py3 linenums=1 hl_lines="5"}
    t=np.linspace(1,10,100)
    g=Medida(9.5,0.5)
    y=(g/2)*(t**2)
    plt.plot(t,Nominais(y),color='r')
    plt.fill_between(t,CurvaMin(y),CurvaMax(y),alpha=0.3)
    #...
```

![Image](queda_livre.png)

## Sigma customizável

O modelo estátistico usado para essas curvas limites está explicitado abaixo

```{.py3}
    CurvaMin = Nominais(dados) - 2*Incertezas(Dados)
    CurvaMin = Nominais(dados) + 2*Incertezas(Dados)
```

Isso implica que as margens de erro são, por padrão, configuradas para um valor de `sigma=2`. No entanto, as funções CurvaMin e CurvaMax aceitam um argumento opcional sigma que permite personalizar esse valor. O exemplo anterior é refeito abaixo com diferentes valores de sigma:

```{.py3 linenums=1 hl_lines="5-8"}
t=np.linspace(1,10,100)
    g=Medida(9.5,0.5)
    y=(g/2)*(t**2)
    plt.plot(t,Nominais(y),color='r')
    plt.fill_between(t,CurvaMin(y),CurvaMax(y),alpha=0.3,label="Sigma = 2")
    plt.fill_between(t,CurvaMin(y,sigma=3),CurvaMax(y,sigma=3),color='b',alpha=0.15,label="Sigma =3")
    plt.fill_between(t,CurvaMin(y,sigma=4),CurvaMax(y,sigma=4),color='g',alpha=0.15,label="Sigma =4")
    plt.fill_between(t,CurvaMin(y,sigma=5),CurvaMax(y,sigma=5),color='m',alpha=0.15,label="Sigma =5")
    #...
```
    ![Image](queda_livre_sigmas.png)