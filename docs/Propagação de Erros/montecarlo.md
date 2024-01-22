## O que é o Monte Carlo?

O método de Monte Carlo consiste em  simular eventos aleatórios 
computacionalmente, ele é especialmente útil para casos que uma resposta analítica nem sempre é conhecida. 
Nessa biblioteca ele é usado
para 'repetir' várias vezes o mesmo experimento do laboratório e encontrar a gama de diferentes respostas esperadas, com essa distribuição é possível calcular uma média \(\mu\) e um 
desvio padrão \(\sigma\) da Medida 
```{.py3 title=LabIFSC2.medida.montecarlo}
def montecarlo(func : callable, *parametros  , 
               hist : bool=False,
               probabilidade : list[float] =False):
```
:::LabIFSC2.medida.montecarlo
## Exemplos
```{.py3 title="Exemplo com \(sin(xy)\)"}
    x=Medida(3,1e-3)
    y=Medida(5,2e-3)
    func=lambda x,y: np.sin(x*y)
    montecarlo(func,x,y) #(-0.65 ± 0.01)
    #Que é o mesmo que fazer
    sin(x**y) #(-0.65 ± 0.01)
    montecarlo(func,x,y,probabilidade=[0.64,0.66]) #0.9032
    histograma=montecarlo(func,x,y,hist=True)
    plt.hist(histograma,bins=50)
    plt.xlabel('Valor encontrado')
    plt.ylabel('Número de repetições')
    plt.savefig('exemplo_histograma.jpg')
```
Abaixo se encontra um histograma dos resultados encontrados,
pelas incertezas serem pequenas é encontrada uma distribuição
parecida com uma gaussiana
![Image](exemplo_histograma.jpg)