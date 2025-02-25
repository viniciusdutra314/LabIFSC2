import numpy as np
import pytest

import LabIFSC2 as lab


def test_probabilidade_analitico():
    x=lab.Medida(0,'mm',1)
    assert np.isclose(x.probabilidade_de_estar_entre(-1,1,'mm'),0.68,1e-2)
    assert np.isclose(x.probabilidade_de_estar_entre(-2,2,'mm'),0.95,1e-2)
    assert np.isclose(x.probabilidade_de_estar_entre(-3,3,'mm'),0.997,1e-3)

    y=lab.Medida(0,'s',1)
    a,b=y.intervalo_de_confiança(0.68,'s')
    assert np.isclose(a,-1,1e-2) and np.isclose(b,1,1e-2)
    a,b=y.intervalo_de_confiança(0.95,'s')
    assert np.isclose(a,-2,atol=0.05) and np.isclose(b,2,atol=0.05)
    a,b=y.intervalo_de_confiança(0.997,'s')
    assert np.isclose(a,-3,atol=0.05) and np.isclose(b,3,atol=0.05)
    with pytest.raises(ValueError):
        y.intervalo_de_confiança(1.1,'s')
    with pytest.raises(ValueError):
         y.intervalo_de_confiança(0,'s')
    with pytest.raises(ValueError):
        y.intervalo_de_confiança(-1,'s')
    y.intervalo_de_confiança(1,'s')
def test_probabilidade_unidade_errada():
    x=lab.Medida(0,'ly',1)
    with pytest.raises(ValueError):
        x.probabilidade_de_estar_entre(-1,1,'s')

def test_probabilidade_e_intervalo_de_confianca():
    x=lab.Medida(4,'s',0.3)
    y=lab.Medida(4,'s',0.3)
    z=x*y
    for p in np.linspace(0.01,1,10):
        x_min,x_max=z.intervalo_de_confiança(p,'s²')
        assert np.isclose(z.probabilidade_de_estar_entre(x_min,x_max,'s²'),p,atol=1e-4) 

    with pytest.raises(ValueError):
        z.probabilidade_de_estar_entre(6,3,'s²')