O LabIFSC2 aceita duas formatações para classe [Medida](../Medidas/Medida.md), uma
formatação facilmente legível e outra para ser usado no LaTeX.

```{.py3 title='Tipos de formatação'}
import LabIFSC2 as lab
x=lab.Medida(15,0.1,'m')
print(x) #(1.50 ± 0.01)E1 m
print(f'{x:latex}') #(1.50 \pm 0.01) \times 10^{1} \, \text{m}
```
A segunda representação renderizada em LaTeX é \((1.50 \pm 0.01) \times 10^{1} \, \text{m}\)

## No console
Caso esteja rodando o código em um console python você notará que caso
não utilize a função print, a Medida será apresentada de forma diferente, 
essa formatação é chamada __repr__ e mostra os valores exatos guardados no objeto
```{.py3 title='Representação console'}
import LabIFSC2 as lab
lado=lab.Medida(5,0.1,'cm')
lado**2
Medida(nominal=25.011305665057893,incerteza=1.010621684513492,unidade='cm2')
```

## Alterar potência
Por padrão o expoente será escolhido para que a mantissa esteja entre 1 e 10,
é possível alterar isso acrescentando E{expoente} na formatação.

```{.py3 title='Mudando a base'}
import LabIFSC2 as lab
x=lab.Medida(456,0.3,'nm')
print(f'{x:latex}') #(4.560 \pm 0.003) \times 10^{2} \, \text{nm}
print(f'{x}') #(4.560 ± 0.003)E2 nm

print(f'{x:latex_E0}') #(456.0 \pm 0.3)\, \text{nm}
print(f'{x:E0}')#(456.0 ± 0.3) nm

```
\((4.560 \pm 0.003) \times 10^{2} \, \text{nm} = (456.0 \pm 0.3)\, \text{nm}\)
## Remover o arredondamento
O arredondamento padrão utilizado é truncar o valor nominal até o primeiro
algarismo significativo da incerteza, os valores completos estão armazenados nos 
atributos *.nominal* , *.incerteza* e para printar esses valores basta adicionar
*full*
```{.py3 title='Sem arredondamento'}
import LabIFSC2 as lab
x=lab.Medida(21.53,1,'cm')
print(f'{x:latex}') #(2.2 \pm 0.1) \times 10^{1} \, \text{cm}
print(x) #(2.2 ± 0.1)E1 cm

print(f'{x:latex_full}') #(2.153 \pm 0.1) \times 10^{1} \, \text{cm}
print(f'{x:full}') #(2.153 ± 0.1)E1 cm
```


## Tudo junto
Os formatadores *latex,full,E* podem ser usados simultaneamente, 
a ordem é irrelevante 
```{.py3 title='Sem arredondamento'}
import LabIFSC2 as lab
x=lab.Medida(21.53,1,'cm')
print(f'{x:latex_full_E0}') #(21.53 \pm 1.0)\, \text{cm}
print(f'{x:E3_full}') #(0.02153 ± 0.001)E3 cm
```
