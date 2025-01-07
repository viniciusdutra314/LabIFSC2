import LabIFSC2 as lab
import numpy as np
import pytest

def test_dimensoes_incompativeis():
    x=lab.Medida(10,1,"m")
    y=lab.Medida(10,1,"s")
    with pytest.raises(ValueError):
        x+y
    z=lab.Medida(55,0.1,'cm')
    w=x+z
    w.converter_para('m')
    assert np.isclose(w.nominal,10.55)
    assert np.isclose(w.incerteza,1)

def test_dimensoes_multiplicacao():
    x=lab.Medida(53,1,"C")
    y=lab.Medida(10,0.1,'mC')
    z=3*x+y
    assert (3*x).unidade=='coulomb'
    assert np.isclose((z).nominal,159.01) 
    assert z.unidade=='coulomb'
    