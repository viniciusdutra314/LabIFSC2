import numpy as np
import pytest
from scipy.optimize import curve_fit

import LabIFSC2 as lab


def test_MExponencial_valores():
    a,k,base=lab.Medida(1,0.1,''),lab.Medida(3,0.01,''),np.exp(1)
    exponencial=lab.MExponencial(a,k,base)
    assert exponencial.a.nominal==a.nominal
    assert exponencial.k.nominal==k.nominal
    assert exponencial.base==base
    a_armazenado,k_armazenado,base_armazenado=exponencial
    assert a_armazenado.nominal==a.nominal
    assert k_armazenado.nominal==k.nominal
    assert base_armazenado==base
    
def test_MExponencial_call():
    a,k,base=lab.Medida(1,0.001,''),lab.Medida(3,0.01,''),np.exp(1)
    exponencial=lab.MExponencial(a,k,base)
    x=lab.Medida(2,0.1,'')
    exponencial(x)
    x_array=lab.linspace(0,1,10,0.1,'')
    exponencial(x_array)

@pytest.mark.parametrize("a, k", [
    (3.6, 1.05),
    (2.0, 0.5),
    (1.0, -2.0),
    (4.5, -0.75),
    (3.0, 1.5),
    (1,0)
])
def test_equivalencia_com_scipy(a, k):
    exponencial_lab = lambda x, a, k: a * lab.exp(k * x)
    exponencial_np = lambda x, a, k: a * np.exp(k * x)

    ruido = np.random.normal(1, 0.001, 100)
    x_dados = np.linspace(3, 10, 100)
    y_dados = exponencial_lab(x_dados, a, k) * ruido
    popt, pcov = curve_fit(exponencial_np, x_dados, y_dados, p0=[a, k])  
    a_scipy, k_scipy = popt
    perr = np.sqrt(np.diag(pcov))
    a_scipy = lab.Medida(a_scipy, perr[0], '')
    k_scipy = lab.Medida(k_scipy, perr[1], '')

    x_dados = lab.linspace(3, 10, 100, 0.01, '')
    y_dados = exponencial_lab(x_dados, a, k) * ruido
    exponencial_lab = lab.regressao_exponencial(x_dados, y_dados)

    assert np.isclose(a_scipy.nominal,exponencial_lab.a.nominal,atol=(1e-2)*a)
    assert np.isclose(k_scipy.nominal,exponencial_lab.k.nominal,atol=(1e-2))
    assert np.isclose(a,exponencial_lab.a.nominal,rtol=1e-2) or np.isclose(a,exponencial_lab.a.nominal,atol=1e-2) 
    assert np.isclose(k,exponencial_lab.k.nominal,rtol=1e-2) or np.isclose(k,exponencial_lab.k.nominal,atol=1e-2) 




def test_exceptions():
    y=lab.linspace(-3,1,10,0.1,'')
    x=lab.linspace(3,1,10,0.1,'')
    
    with pytest.raises(ValueError):
        lab.regressao_exponencial(x,y)
    lab.regressao_exponencial(y,x)
    with pytest.raises(ValueError):
        lab.regressao_exponencial(x,x,base=0.8)