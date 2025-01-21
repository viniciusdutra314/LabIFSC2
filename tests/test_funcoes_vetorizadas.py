import numpy as np
import pytest

import LabIFSC2 as lab


def test_array_medida_soma():
    x=lab.Medida(0,0.0001,'')
    x_array=lab.linspaceM(0,10,10,0.001,'')
    somar=x+x_array
    assert isinstance(somar,np.ndarray)
    somar=x_array+x
    assert isinstance(somar,np.ndarray)
    for soma in somar:
        assert isinstance(soma,lab.Medida)
    for index, soma in enumerate(somar):
        assert np.isclose(soma.nominal(""),x_array[index].nominal(""),rtol=1e-2)

def test_array_medida_subtracao():
    x = lab.Medida(10, 0.0001, '')
    x_array = lab.linspaceM(1, 10, 10, 0.1, '')
    subtrair = x - x_array
    assert isinstance(subtrair, np.ndarray)
    subtrair = x_array - x
    assert isinstance(subtrair, np.ndarray)
    for diferenca in subtrair:
        assert isinstance(diferenca, lab.Medida)
    for index, diferenca in enumerate(subtrair):
        assert np.isclose(diferenca.nominal(""), x_array[index].nominal("")-10, rtol=1e-3)



def test_array_medida_multiplicacao():
    x = lab.Medida(2, 0.0001, '')
    x_array = lab.linspaceM(1, 10, 10, 0.1, '')
    multiplicar = x * x_array
    assert isinstance(multiplicar, np.ndarray)
    multiplicar = x_array * x
    assert isinstance(multiplicar, np.ndarray)
    for produto in multiplicar:
        assert isinstance(produto, lab.Medida)
    for index, produto in enumerate(multiplicar):
        assert np.isclose(produto.nominal(""),2*x_array[index].nominal(""), rtol=1e-3)

def test_array_medida_divisao():
    x = lab.Medida(13, 0.001, '')
    x_array = lab.linspaceM(1, 10, 10, 0.1, '')
    dividir = x / x_array
    assert isinstance(dividir, np.ndarray)
    dividir = x_array / x
    assert isinstance(dividir, np.ndarray)
    for quociente in dividir:
        assert isinstance(quociente, lab.Medida)
    for index, quociente in enumerate(dividir):
        assert np.isclose(quociente.nominal(""),  x_array[index].nominal("")/13, rtol=1e-3)
