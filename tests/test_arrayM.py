import numpy as np
import pytest

from LabIFSC2 import (Medida, arrayM, curva_max, curva_min, incertezas,
                      linspaceM, nominais)


def test_nominal():
    x=np.array([Medida(13431,351,''),Medida(0.006132,4,''),
                Medida(-34,3,''),Medida(-5313.351,3,'')])
    nominal=nominais(x,'')
    assert nominal[0]==13431
    assert nominal[1]==0.006132
    assert nominal[2]==-34
    assert nominal[3]==-5313.351
    with pytest.raises(TypeError):
        nominais(np.arange(10))

def test_incerteza_array():
    x=np.array([Medida(-351,3.5,''),Medida(0.006132,4.003,''),
                Medida(-34,310,''),Medida(-5313.351,0,'')])
    incerteza=incertezas(x,'')
    assert incerteza[0]==3.5
    assert incerteza[1]==4.003
    assert incerteza[2]==310
    assert incerteza[3]==0
    with pytest.raises(TypeError):
        incertezas(np.arange(10),'')
        

def test_curvamin():
    t=np.array([Medida(5,0.1,''),Medida(9,2,''),Medida(11,0.5,'')])
    curva_min(t,'')
    assert np.array_equal(curva_min(t,''),np.array([4.8,5,10]))
    assert np.array_equal(curva_min(t,'',3),np.array([4.7,3,9.5]))  
    with pytest.raises(TypeError):
        curva_min(np.arange(10),"")
def test_curvamax():
    t=np.array([Medida(5,0.1,''),Medida(9,2,''),Medida(11,0.5,'')])
    assert np.array_equal(curva_max(t,""),np.array([5.2,13,12]))
    assert np.array_equal(curva_max(t,"",3),np.array([5.3,15,12.5]))      
    with pytest.raises(TypeError):
        curva_max(np.arange(10),"")

def test_linspace():
    a=1 ; b=20 ; N=20
    x=linspaceM(a,b,N,0.1,'')
    assert np.all(nominais(x,"")==np.linspace(a,b,N))
    assert np.all(incertezas(x,"")==0.1)


def test_converter_array():
    x=linspaceM(5,10,10,0.01,'mm')
    esperado=np.linspace(0.5,1,10) #cm
    for index in range(len(x)):
        assert np.isclose(x[index].nominal('cm'),esperado[index])

def test_converter_array_si():
    x=linspaceM(10,50,10,0.01,'cm')
    esperado=np.linspace(0.1,0.5,10) #si
    for index in range(len(x)):
        assert np.isclose(x[index].nominal('si'),esperado[index])

def test_array_m():
    x_dados=arrayM([1,2,3,4,5],0.01,'s')
    for i in range(len(x_dados)):
        assert x_dados[i].nominal('s')==i+1
        assert x_dados[i].incerteza('s')==0.01
    with pytest.raises(TypeError):
        arrayM(x_dados,0.01,'km/s')