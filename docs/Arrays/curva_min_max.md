:::LabIFSC2.operacoes_em_arrays.curva_min


As funções `curva_min` e `curva_max` são usadas na criação de gráficos com propagação de erro em curvas, elas recebem um array de Medidas e retornam um array com a curva máximo/mínima,abaixo consta um gráfico de uma queda livre usando Matplotlib e gravidade com valor \((9.5 \pm 0.5)ms^{-2}\) . 

```{.py3 linenums=1 hl_lines="5"}
    import numpy as np
    import LabIFSC2 as lab
    t=np.linspace(1,10,100)
    g=lab.Medida(9.5,0.5)
    y=(g/2)*(t**2)
    plt.plot(t,lab.get_nominais(y),color='r')
    plt.fill_between(t,lab.curva_min(y),
                    lab.curva_max(y),alpha=0.3)
    #...
```

![Image](queda_livre.png)

## Sigma customizável

O modelo estatístico usado para essas curvas limites está explicitado abaixo

```{.py3}
    curva_min=lab.get_nominais(arrayM) - 2*lab.get_incertezas(arrayM)
    curva_max=lab.get_nominais(arrayM) + 2*lab.get_incertezas(arrayM)
```

Isso implica que as margens de erro são, por padrão, configuradas para um valor de `sigma=2`. No entanto, as funções curva_min e curva_max aceitam um argumento opcional sigma que permite personalizar esse valor. O exemplo anterior é refeito abaixo com diferentes valores de sigma:

```{.py3}
    plt.fill_between(t,lab.curva_min(y,sigma=3),
    lab.curva_max(y,sigma=3),color='b',alpha=0.15,label="Sigma =3")

    plt.fill_between(t,lab.curva_min(y,sigma=4),
    lab.curva_max(y,sigma=4),color='g',alpha=0.15,label="Sigma =4")

    plt.fill_between(t,lab.curva_min(y,sigma=5),
    lab.curva_max(y,sigma=5),color='m',alpha=0.15,label="Sigma =5")
    #...
```
    ![Image](queda_livre_sigmas.png)
