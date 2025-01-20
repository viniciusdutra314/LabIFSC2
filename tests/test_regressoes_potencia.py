import numpy as np
import pytest
from scipy.optimize import curve_fit

import LabIFSC2 as lab


@pytest.mark.parametrize("a, b", [
    (3.6, 1.05),
    (2.0, 0.5),
    (1.0, -2.0),
    (4.5, -0.75),
    (3.0, 1.5),
    (1,0.05)
])
def test_lei_de_potencia(a, b):
    potencia_lab = lambda x, a, b: a * lab.pow(x, b)
    potencia_np = lambda x, a, b: a * np.power(x, b)

    ruido = np.random.normal(1, 0.002, 100)
    x_dados = np.linspace(3, 10, 100)
    y_dados = potencia_lab(x_dados, a, b) * ruido
    popt,   pcov = curve_fit(potencia_np, x_dados, y_dados)  
    a_scipy, b_scipy = popt

    x_dados = lab.linspace(3, 10, 100, 0.01, '')
    y_dados = potencia_lab(x_dados, a, b) * ruido
    potencia_lab = lab.regressao_potencia(x_dados, y_dados)
    assert np.isclose(a_scipy,potencia_lab.a.nominal(""),atol=(1e-2)*a)
    assert np.isclose(b_scipy,potencia_lab.n.nominal(""),atol=(1e-2))
    assert np.isclose(a,potencia_lab.a.nominal(""),rtol=1e-2) or np.isclose(a,potencia_lab.a.nominal(""),atol=1e-2) 
    assert np.isclose(b,potencia_lab.n.nominal(""),rtol=1e-2) or np.isclose(b,potencia_lab.n.nominal(""),atol=1e-2)


def test_exceptions():
    negativo=lab.linspace(-5,5,11,0.01,'')
    positivo=lab.linspace(5,10,11,0.01,'')

    with pytest.raises(ValueError):
        lab.regressao_potencia(negativo,positivo)
    
    with pytest.raises(ValueError):
        lab.regressao_potencia(positivo,negativo)
    
    with pytest.raises(ValueError):
        lab.regressao_potencia(negativo,negativo)
    lab.regressao_potencia(positivo,positivo)