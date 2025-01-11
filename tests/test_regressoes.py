import LabIFSC as lab1
import LabIFSC2 as lab2
import numpy as np

def test_regressao_linear():

    for _ in range(10):
        num=10
        a,b=np.random.normal(0,1,(2,num))
        x=np.arange(num)
        y=a*x+b
        resposta=lab1.linearize(x,y)
        
        
        x_dados=lab2.arrayM(x,0.01,'s')
        y_dados=lab2.arrayM(y,0.01,'m')
        reta=lab2.regressao_linear(x_dados,y_dados)
        a,b=reta
        print(a.nominal,resposta['a'])
        print(b.nominal,resposta['b'])
        assert np.isclose(a.nominal,resposta['a'],rtol=1e-3)
        assert np.isclose(b.nominal,resposta['b'],rtol=1e-3)
        print(a.incerteza,resposta['Δa'])
        print(b.incerteza,resposta['Δb'])
        assert np.isclose(a.incerteza,resposta['Δa'],rtol=1e-3)
        assert np.isclose(b.incerteza,resposta['Δb'],rtol=1e-3)