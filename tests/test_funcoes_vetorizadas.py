import numpy as np
import pytest

import LabIFSC2 as lab


def test_funcoes_customizadas():
    x=lab.Medida(0,0.01,'')
    sinc=lambda x: np.sin(x)/x
    with pytest.raises(TypeError):
        sinc(x)
    lab_sinc=lab.aceitamedida(sinc)
    assert np.isclose(lab_sinc(x).nominal,1,rtol=1e-4)
    x_array=lab.linspace(0.1,10,10,0.001,'')
    aplicado=lab_sinc(x_array)
    for i in range(len(aplicado)):
        assert np.isclose(aplicado[i].nominal,
                          sinc(x_array[i].nominal),rtol=1e-4)

