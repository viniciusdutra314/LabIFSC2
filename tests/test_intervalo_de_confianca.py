import LabIFSC2 as lab
import numpy as np
import pytest


def test_probabilidade_analitico():
    x=lab.Medida(0,1,'mm')
    assert np.isclose(x.probabilidade_de_estar_entre(-1,1,'mm'),0.68,1e-2)
    assert np.isclose(x.probabilidade_de_estar_entre(-2,2,'mm'),0.95,1e-2)
    assert np.isclose(x.probabilidade_de_estar_entre(-3,3,'mm'),0.997,1e-3)

def test_probabilidade_unidade_errada():
    x=lab.Medida(0,1,'ly')
    with pytest.raises(ValueError):
        x.probabilidade_de_estar_entre(-1,1,'s')

def test_probabilidade_e_intervalo_de_confianca():
    x=lab.Medida(4,0.3,'s')
    y=lab.Medida(4,0.3,'s')
    z=x*y
    for p in np.linspace(0.01,1,10):
        x_min,x_max=z.intervalo_de_confianca(p)
        assert np.isclose(z.probabilidade_de_estar_entre(x_min,x_max,'s²'),p,atol=1e-4) 