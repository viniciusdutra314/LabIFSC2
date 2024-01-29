O LabIFSC2 aceita duas formatações para classe [Medida](../Medidas/Medida.md), uma
formatação facilmente legível no console e outra para ser usado no LaTeX.

```{.py3 title='Tipos de formatação'}
    import LabIFSC2 as lab
    x=lab.Medida(15,0.1,'m')
    print(x) #(1.50 ± 0.01)E1 m
    print(f'{x:latex}') #(1.50 \pm 0.01) \times 10^{1} \, \text{m}
```
A segunda representação em LaTeX é \((1.50 \pm 0.01) \times 10^{1} \, \text{m}\), por
padrão o expoente será escolhido para que a mantissa esteja entre 1 e 10, mas isso
é possível alterar acrescentando E{expoente} na formatação.


```{.py3 title='Mudando a base da formatação'}
    import LabIFSC2 as lab
    x=lab.Medida(456,0.3,'nm')
    print(f'{x:latex}') #(4.560 \pm 0.003) \times 10^{2} \, \text{nm}
    print(f'{x:latexE0}') #(456.0 \pm 0.3)\, \text{nm}
```

\((4.560 \pm 0.003) \times 10^{2} \, \text{nm} = (456.0 \pm 0.3)\, \text{nm}\)


Caso queira adicionar uma nova representação basta ler a secção [Nova formatação](../Como_contribuir?.md) de Como Contribuir?