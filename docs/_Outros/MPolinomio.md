## Polinômios de Medidas
Baseada na classe [Polynominal](https://numpy.org/doc/stable/reference/routines.polynomials.html#) do Numpy, a classe *MPolinomio* trabalha com polinômios \(p(x)\) que tanto os coeficientes quanto \(x\) podem ser Medidas.

```{.py3 title="Criação de um MPolinomio"}
    coefs=[Medida(6,0.01),Medida(-5,0.2),Medida(1,0.1)]
    p=Polinomio(coefs)
    print(p)#(6.00 ± 0.01)  - (5.0 ± 0.2) ·x + (1.0 ± 0.1) ·x²
```
Podemos usar esse polinômio como se fosse uma função e calcularmos
em um \(x\), por exemplo \(x=1\), ou até um valor com incerteza.

```{.py3 title="MPolinomio como funções"}
print(p(1)) #(2.0 ± 0.2)
print(p(Medida(1,0.2))) #(2 ± 1) 
```

## Operações Elementares
É possível realizar operações elementares entre polinômios,
```{.py3 title=Soma/Subtração entre MPolinomios}
    coefs1=[Medida(6,0.01),Medida(-5,0.2),Medida(1,0.1)]
    coefs2=[Medida(85,0.01),Medida(3,0.2),Medida(-7,0.1)]
    p1=MPolinomio(coefs1)
    p2=MPolinomio(coefs2)
    print(p1+p2)#(9.100 ± 0.001)E1  -(2.0 ± 0.3) ·x -(6.0 ± 0.1)·x²
    print(p1-p2)#(-7.900 ± 0.001)E1  - (8.0 ± 0.3) ·x +(8.00 ± 0.10) ·x²
```

```{.py3 title=Multiplicação entre MPolinomios}
coefs=[Medida(1,0.2),Medida(1,0.1)]
p=MPolinomio(coefs)
print(p**2) #(1.0 ± 0.3) +(2.0 ± 0.3) ·x + (1.0 ± 0.1) ·x²
coefs_1=[Medida(2,0.2),Medida(1,0.1)]
coefs_2=[Medida(3,0.2),Medida(1,0.1)]
p1=MPolinomio(coefs_1)
p2=MPolinomio(coefs_2)
print(p1*p2)  #(6 ± 1) +(5.0 ± 0.5) ·x + (1.0 ± 0.1) ·x²
```
### Operações NÃO elementares

### Derivadas

### Retornar Coeficientes
Os MPolinomios possuem um atributo chamado coef que
é um array numpy com os coeficientes, no caso de Medidas
é retornado um array de Medidas, abaixo consta um código
simples que calcula um triângulo de Pascal usando a 
expansão de \((1+x)^n\)
```{.py3 title=Triângulo de Pascal}
    p=MPolinomio([1,1])
    for n in range(6):
        print((p**n).coef) 
    #[1.]
    #[1. 1.]
    #[1. 2. 1.]
    #[1. 3. 3. 1.]
    #[1. 4. 6. 4. 1.]
    # [ 1.  5. 10. 10.  5.  1.]
```
### Raizes do MPolinomio