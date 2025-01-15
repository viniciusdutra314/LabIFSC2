::: LabIFSC2.regressões.regressao_potencia


Leis de potência são relações da forma \(y=Ax^n\)

Sabemos por exemplo que fixados as massas \(M\) e \(m\), a força gravitacional entre dois corpos é uma constante vezes alguma relação com a distância \(g=Ar^n\), fazendo esse tipo de regressão encontraríamos algo como \(n \approx 2\), que é a lei do inverso do quadrado.

No exemplo abaixo pegamos a distância (UA=unidade astronômica) e período (ano) dos primeiros 5 planetas do sistema solar, e calculamos a melhor lei de potência entre essas duas grandezas. 

Obtemos \(n=(1.493\pm 0.01)\), pela lei de Kepler temos \(T=Ar^{1.5}\) que é muito próximo do experimental.

```{.py3 title="Exemplo Lei de Kepler"}
    periodos=np.array([0.24,0.61,1.00,1.88,11.86])
    distancias=np.array([0.38,0.72,1.00,1.52,5.20])
    a,n=regressao_potencia(distancias,periodos)
    #periodo=(1.006+-0.005)*distancia^{1.5}
```



