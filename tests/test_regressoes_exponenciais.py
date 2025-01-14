import numpy as np
import pytest

import LabIFSC2 as lab


def test_MExponencial_valores():
    a,k,base=1,3,np.exp(1)
    exponencial=lab.MExponencial(a,k,base)
    assert exponencial.a==a
    assert exponencial.k==k
    assert exponencial.base==base
    a_armazenado,k_armazenado,base_armazenado=exponencial
    assert a_armazenado==a
    assert k_armazenado==k
    assert base_armazenado==base
    
def test_MExponencial_call():
    a,k,base=1,3,np.exp(1)
    exponencial=lab.MExponencial(a,k,base)
    x=2
    assert np.isclose(exponencial(x),1*np.exp(3*2))
