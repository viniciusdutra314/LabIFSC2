Como demonstrada na secção [Monte Carlo](monte carlo.md), a incerteza
associada a qualquer função pode ser calculada com esse método, portanto, o LabIFSC2 oferece um decorador conveniente chamado
**aceitamedida**

:::LabIFSC2.matematica.aceitamedida
## Exemplos
Imagine que você precise utilizar a função fatorial \(\Gamma\),
podemos criar uma ponte entre a função definida na biblioteca
scipy e o LabIFSC2
```{.py3 title=Exemplo função gamma}
    from LabIFSC import *
    from scipy.special import gamma
    gamma=aceitamedida(gamma)
    gamma(Medida(5,0.1)) #(24 ± 3)
```
Caso seja uma função definida por você mesmo, é possível
usar a sintaxe mais comum para um decorador
```{.py3 title=Exemplo função gamma}
    @aceitamedida
    def funcao_customizada(x):
        return x*np.exp(-x**2)
    funcao_customizada(Medida(1,0.1))#(3.6±0.4)
```