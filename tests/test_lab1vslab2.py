import LabIFSC as lab1
import LabIFSC2 as lab2
import numpy as np
def igualdade_medida(Medidalab1,Medidalab2):
    Medidalab1=lab2.Medida(Medidalab1.nominal,Medidalab1.incerteza)
    Medidalab2=lab2.Medida(Medidalab2.nominal,Medidalab2.incerteza)
    return Medidalab1 == Medidalab2

def test_somas():
    a=np.random.random(100); b=np.random.random(100)
    c=np.random.random(100); d=np.random.random(100)
    for a,b,c,d in zip(a,b,c,d):
        x=lab1.Medida((a,b))+lab1.Medida((c,d))
        y=lab2.Medida(a,b)+lab2.Medida(c,d)
        assert igualdade_medida(x,y)
        x=lab1.Medida((c,a))-lab1.Medida((d,b))
        y=lab2.Medida(c,a)-lab2.Medida(d,b)
        assert igualdade_medida(x,y)
def test_multiplicacao():
    a=np.random.random(100); b=np.random.random(100)/20
    c=np.random.random(100); d=np.random.random(100)/20
    for a,b,c,d in zip(a,b,c,d):
        x=lab1.Medida((a,b))*lab1.Medida((c,d))
        y=lab2.Medida(a,b)*lab2.Medida(c,d)
        assert igualdade_medida(x,y)

def test_funcoes_matematicas():
    nominais=np.random.random(100)
    incertezas=np.random.random(100)/100
    for nominal,incerteza in zip(nominais,incertezas):
        x=lab1.sin(lab1.Medida((nominal,incerteza)))
        y=lab2.sin(lab2.Medida(nominal,incerteza))
        assert igualdade_medida(x,y.item())
        x=lab1.cos(lab1.Medida((nominal,incerteza)))
        y=lab2.cos(lab2.Medida(nominal,incerteza))
        assert igualdade_medida(x,y.item())
