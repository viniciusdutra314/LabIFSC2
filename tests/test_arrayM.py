import numpy as np

from LabIFSC2 import (Medida, curva_max, curva_min, exp, get_incertezas,
                      get_nominais, linspace, sin,)



def test_nominal():
    x=np.array([Medida(13431,351,''),Medida(0.006132,4,''),
                Medida(-34,3,''),Medida(-5313.351,3,'')])
    nominal=get_nominais(x)
    assert nominal[0]==13431
    assert nominal[1]==0.006132
    assert nominal[2]==-34
    assert nominal[3]==-5313.351


def test_incerteza_array():
    x=np.array([Medida(-351,3.5,''),Medida(0.006132,4.003,''),
                Medida(-34,310,''),Medida(-5313.351,0,'')])
    incerteza=get_incertezas(x)
    assert incerteza[0]==3.5
    assert incerteza[1]==4.003
    assert incerteza[2]==310
    assert incerteza[3]==0

def test_curvamin():
    t=np.array([Medida(5,0.1,''),Medida(9,2,''),Medida(11,0.5,'')])
    assert np.array_equal(curva_min(t),np.array([4.8,5,10]))
    assert np.array_equal(curva_min(t,3),np.array([4.7,3,9.5]))  

def test_curvamax():
    t=np.array([Medida(5,0.1,''),Medida(9,2,''),Medida(11,0.5,'')])
    assert np.array_equal(curva_max(t),np.array([5.2,13,12]))
    assert np.array_equal(curva_max(t,3),np.array([5.3,15,12.5]))      

def test_linspace():
    a=1 ; b=20 ; N=20
    x=linspace(a,b,N,0.1,'')
    assert np.all(get_nominais(x)==np.linspace(a,b,N))
    assert np.all(get_incertezas(x)==0.1)
