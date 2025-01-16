import numpy as np
import pytest

import LabIFSC2 as lab


def test_soma():
    
    x,y=lab.Medida(0,0.1,''),lab.Medida(5,0.3,'')
    assert (x+y).nominal==5
    assert (x+y).incerteza==np.sqrt(0.1**2+0.3**2)

    assert (y+x).nominal==5
    assert (y+x).incerteza==np.sqrt(0.1**2+0.3**2)

    assert (x-y).nominal==-5
    assert (x-y).incerteza==np.sqrt(0.1**2+0.3**2)

    assert (y-x).nominal==5
    assert (y-x).incerteza==np.sqrt(0.1**2+0.3**2)

    assert (x-x).nominal==0 and (x-x).incerteza==0
    assert (y-y).nominal==0 and (y-y).incerteza==0
    z=lab.Medida(5,0.01,'')*lab.Medida(5,0.01,'')
    w=lab.Medida(5,0.01,'')
    assert np.isclose((z+w).nominal,30,1e-4)
    assert np.isclose((z-w).nominal,20,1e-4)


def test_multiplicacao_medidas():
    x=lab.Medida(0,0.1,'')
    y=lab.Medida(0,0.1,'')
    correlacionado=x*x
    nao_correlacionado=lab.montecarlo(lambda a,b: a*b,x,y)
    assert not (np.any(correlacionado)<0)
    assert np.any(nao_correlacionado._histograma>0) and np.any(nao_correlacionado._histograma<0)
    assert not (correlacionado._gaussiana and nao_correlacionado._gaussiana)
    w=lab.Medida(0,0.1,'')
    assert lab.comparar_medidas(w*x,nao_correlacionado)==lab.Comparacao.EQUIVALENTES

def test_multiplicacao_cte():
    x=lab.Medida(5,0.1,'')
    y=3*x
    assert y.nominal==15 and y.incerteza==0.1*3
    y=(-3)*x
    assert y.nominal==-15 and y.incerteza==0.1*3

    y=x*3
    assert y.nominal==15 and y.incerteza==0.1*3
    y=x*(-3)
    assert y.nominal==-15 and y.incerteza==0.1*3


def test_mudanca_de_sinal():
    x=lab.Medida(5,0.1,'')
    y=-x
    assert y.nominal==-5 and y.incerteza==0.1
    y=abs(y)
    assert y.nominal==5 and y.incerteza==0.1
    w=abs(x/y)
    assert np.isclose(w.nominal,1,rtol=1e-3)
    
    
    z=+w
    for i in range(len(z._histograma)):
        assert z._histograma[i]==w._histograma[i]
    z=-w
    for i in range(len(z._histograma)):
        assert z._histograma[i]==-w._histograma[i]

def test_divisao():
    x=lab.Medida(-3,0.1,'')
    correlacao=x/x
    assert correlacao.nominal==1 and correlacao.incerteza==0

    x=lab.Medida(5,0.1,'')
    assert (x/5).nominal==1 and (x/5).incerteza==0.1/5 

    y=lab.Medida(-3,0.1,'')
    assert (x/y).incerteza!=0

    assert np.isclose((10/x).nominal,2,1e-3)

    divisao=(y/x).nominal
    divisao_inversa=(x/y).nominal
    assert np.isclose(divisao,1/divisao_inversa,rtol=1e-2)


    with pytest.raises(TypeError):
        '3'/lab.Medida(0,0.1,'')

def test_divisoes_especiais_nao_existe():
    statements=[lambda x,y: x//y,lambda x,y: x%y,lambda x,y: divmod(x,y)]
    with pytest.raises(TypeError):
        for statement in statements:
            statement(lab.Medida(6,0.1,''),lab.Medida(1,0.1,''))


def test_potencia():
    x=lab.Medida(2,0.01,'')
    y=lab.Medida(6,0.01,'')
    assert np.isclose((x**3).nominal,8,1e-3) 
    assert np.isclose((2**x).nominal,4,1e-3) 
    assert np.isclose((x**y).nominal,64,1e-2)
    assert (x**y).incerteza>(x**2).incerteza
    assert np.isclose((x**-20).nominal,1/(2**20),1e-3)
    with pytest.raises(TypeError):
        lab.Medida(0,0.1,'')**'3'
    with pytest.raises(TypeError):
        '3'**lab.Medida(0,0.1,'')