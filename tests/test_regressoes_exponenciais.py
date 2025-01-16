import numpy as np
import pytest

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
    x=2
    exponencial(x)
    x_array=np.linspace(1,3,10)
    exponencial(x_array)
    