import numpy as np
import pint
import pytest

import LabIFSC2 as lab


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

def test_trignometria():
    x = lab.Medida(45, 1, "m")
    with pytest.raises(pint.errors.DimensionalityError):
        lab.sin(x)
    with pytest.raises(pint.errors.DimensionalityError):
        lab.cos(x)
    with pytest.raises(pint.errors.DimensionalityError):
        lab.tan(x)
    x = lab.Medida(45, 1, "rad")
    lab.sin(x)
    lab.cos(x)
    lab.tan(x)

def test_angulos_notaveis():
    x=lab.sin(lab.Medida(45,0.01,'degree'))
    y=lab.cos(lab.Medida(60,0.01,'degree'))
    assert np.isclose(x.nominal,1/np.sqrt(2),rtol=1e-4)
    assert np.isclose(y.nominal,1/2,rtol=1e-4)

def test_exponencial_unidade():
    x=lab.Medida(1,0.01,'m')
    with pytest.raises(pint.errors.DimensionalityError):
        lab.exp(x)
    with pytest.raises(pint.errors.DimensionalityError):
        lab.ln(x)

def test_soma_graus():
    theta=lab.Medida(45,0.01,'degree')
    theta2=lab.Medida(1,0.01,'radian')
    theta_soma=theta+theta2
    assert np.isclose(theta_soma.nominal,1+0.785398,rtol=1e-2)
    theta_soma.converter_para('degree')
    assert np.isclose(theta_soma.nominal,45+57.29,rtol=1e-2)

def test_conversao_interna_histograma():
    x=lab.Medida(1,0.01,'m')
    y=lab.Medida(1,0.01,'cm')
    z=x*y
    z.converter_para('cm²')
    assert z.histograma.units==lab._medida.ureg.cm**2
    z.converter_para_si()
    assert z.histograma.units==lab._medida.ureg.m**2

    x.converter_para('cm')
    assert x.histograma.units==lab._medida.ureg.cm
    assert len(x.histograma)==100_000
    y.converter_para_si()
    assert y.histograma.units==lab._medida.ureg.m
