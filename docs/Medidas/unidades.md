Um objeto da classe Medida possui um argumento opcional chamado **unidade**, 
caso não especificado a Medida será considerada adimensional, a grande
vantagem de especificar a unidade é ter acesso a métodos de conversão e
verificação de unidades!

## Unidade x Dimensão
Durante a documentação será usada as palavras unidade e dimensão que possuem
significados levemente diferentes, usemos como exemplo velocidade
\\(v=\Delta s / \Delta t \\), velocidade possui dimensão de distância por tempo \(L T^{-1}\), unidades que expressam essas dimensões são por exempo \(m/s\) e \(km/h\) , elas são unidades diferentes mas possuem a mesma dimensão 

## Checa dimensão
Todos os métodos entre Medidas são decorados com a função checa_dimensao, portanto,
operações inválidas entre unidades levantaram um ValueError
```{.py3 title='Dimensões incompatíveis'}
    import LabIFSC2 as lab
    x=lab.Medida(3,0.1,'kg')
    y=lab.Medida(10,0.01,'m')
    x+y #ValueError(f"Unidades com dimensões diferentes {unidade}≠{outra_unidade}")

```
## Adição
A soma entre duas Medidas com unidades diferentes porém de mesma dimensão será
convertida para a unidade mais "próximo" do valor total
```{.py3 title='Soma entre unidades diferentes'}
    import LabIFSC2 as lab
    x=lab.Medida(1,0.01,'m')
    y=lab.Medida(20,1,'cm')
    x+y #(1.20 ±0.01) m 

    z=lab.Medida(10,0.1,'km')
    x+z #(1 ± 0.1)E1 km
```
