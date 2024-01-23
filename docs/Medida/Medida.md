A classe central do LabIFSC2 é a Medida, tecnicamente ela 
representa uma variável aleatória gaussiana, portanto,
é necessário fornecer uma média \(\mu\) e um desvio padrão
\(\sigma\), além disso, é possível oferecer uma unidade
e realizar conversões de unidade
### Propagação de Erros
Toda a propagação de erros é implementada usando uma simulação
[Monte Carlo](../Propagação%20de%20Erros/montecarlo.md), em casos
de solução analítica simples é implementada a propagação exata
```{.py3 title='Operações básicas'}
    from LabIFSC2.medida import Medida
    x=Medida(4,0.1)
    y=Medida(0.4,0.05)
    #Operações básicas
    print(x+y)#(4.40 ± 0.10) 
    print(x-y)#(3.60 ± 0.10) 
    print(x*y)#(1.60 ± 0.20) 
    print(x/y)#(1.0 ± 0.1)E1 
    #Exponenciação
    print(x**y)#(1.75 ± 0.10) 
    print(x**2)#(16 ± 1)
    print(3**x)#(81 ± 1)
```
### Atributos
Cada instância da classe Medida possui atributos
associados a média e o desvio padrão, caso
não seja especificado unidades, os atributos
no SI serão iguais aos originais
```{.py3 title='Atributos de uma medida'}
    from LabIFSC2.medida import Medida
    x=Medida(156,2,'cm')
    print(x.nominal)#156
    print(x.si_nominal)#1.56
    print(x.incerteza)#2
    print(x.si_incerteza)#0.02
```
### Compatibilidade com o LabIFSC original
O método tradicional usado no LabIFSC é uma propagação de erros lineares, é usada uma expansão de Taylor com centro em \(\mu\).
No caso que os erros forem pequenos em comparação a variação da função
tanto o LabIFSC quanto o LabIFSC2 chegaram em resultados equivalentes,
testes unitários exatamente sobre isso podem ser encontrados
no [repositório](https://github.com/viniciusdutra314/LabIFSC2/blob/main/tests/test_lab1vslab2.py), eis um exemplo:
:::tests.test_lab1vslab2.test_funcoes_matematicas