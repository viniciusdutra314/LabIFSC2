from LabIFSC2 import Medida,Nominais,Incertezas,CurvaMax,CurvaMin
from LabIFSC2 import exp,sin
import numpy as np  
def test_nominal_lista():
    x=[Medida(1,0.1),Medida(6132,4),Medida(-34,3),Medida(-5313.351)]
    nominal=Nominais(x)
    assert nominal[0]==1
    assert nominal[1]==6132
    assert nominal[2]==-34
    assert nominal[3]==-5313.351
def test_nominal_array():
    x=np.array([Medida(13431,351),Medida(0.006132,4),Medida(-34,3),Medida(-5313.351)])
    nominal=Nominais(x)
    assert nominal[0]==13431
    assert nominal[1]==0.006132
    assert nominal[2]==-34
    assert nominal[3]==-5313.351
def test_nominal_tupla():
    x=(Medida(13431,351),Medida(0.006132,4),Medida(-34,3),Medida(-5313.351))
    nominal=Nominais(x)
    assert nominal[0]==13431
    assert nominal[1]==0.006132
    assert nominal[2]==-34
    assert nominal[3]==-5313.351

def test_incerteza_lista():
    x=[Medida(1,0.1),Medida(6132,4),Medida(-34,3),Medida(-5313.351)]
    incerteza=Incertezas(x)
    assert incerteza[0]==0.1
    assert incerteza[1]==4
    assert incerteza[2]==3
    assert incerteza[3]==0
def test_incerteza_array():
    x=np.array([Medida(-351,3.5),Medida(0.006132,4.003),Medida(-34,310),Medida(-5313.351,0)])
    incerteza=Incertezas(x)
    assert incerteza[0]==3.5
    assert incerteza[1]==4.003
    assert incerteza[2]==310
    assert incerteza[3]==0
def test_incerteza_tupla():
    x=(Medida(13431,351),Medida(0.006132,4),Medida(-34,3),Medida(-5313.351))
    incerteza=Incertezas(x)
    assert incerteza[0]==351
    assert incerteza[1]==4
    assert incerteza[2]==3
    assert incerteza[3]==0

def test_curvamin():
    t=np.array([Medida(5,0.1),Medida(9,2),Medida(11,0.5)])
    assert np.array_equal(CurvaMin(t),np.array([4.8,5,10]))
    assert np.array_equal(CurvaMin(t,3),np.array([4.7,3,9.5]))  

def test_curvamax():
    t=np.array([Medida(5,0.1),Medida(9,2),Medida(11,0.5)])
    assert np.array_equal(CurvaMax(t),np.array([5.2,13,12]))
    assert np.array_equal(CurvaMax(t,3),np.array([5.3,15,12.5]))  
