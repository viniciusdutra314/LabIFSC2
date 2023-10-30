Por incrível que pareça, é possível transformar uma exponencial em uma reta. Temos a relação \(y=ae^{kx}\), considerando somente numeros positivos, podemos aplicar a função \(log\) em ambos os lados, obtendo \(log(y)=log(a)+kx\), se fizermos um gráfico de \(log(y)\) por \(x\), será uma reta!

Como já sabemos calcular a melhor reta ([Regressão Linear](linear.md)), podemos encontrar a melhor reta usando essa transformação e depois convertemos para as variaveis originais.


```{.py3 title="Exemplo Exponencial"}
    x=np.array([0,1,2,3,4,5])
    y=np.array([1,2,3.9,7.85,17,31]) #uma relação quase y=2^x
    a,k=regressao_exponencial(x,y) #(0.99+-0.01)e^(0.693+-0.008)
    a,k=regressao_exponencial(x,y,base=10)#(0.99+-0.01)10^(0.301+-0.003)
```

