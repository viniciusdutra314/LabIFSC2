import numpy as np
import pytest

import LabIFSC2 as lab


def test_initialization():
    coeficientes = np.array([1, 2, 3])
    polinomio = lab.MPolinomio(coeficientes)
    assert np.array_equal(polinomio._coeficientes,coeficientes)
    assert polinomio._grau == 2
    assert polinomio.a == 1
    assert polinomio.b == 2
    assert polinomio.c == 3

def test_call():
    coeficientes = np.array([1, 2, 3])
    polinomio = lab.MPolinomio(coeficientes)
    assert polinomio(0) == 3
    assert polinomio(1) == 6
    assert polinomio(2) == 11

    assert np.array_equal(polinomio(np.array([0,1,2])),np.array([3,6,11]))


def test_str():
    coeficientes = np.array([1, 2, 3],dtype=object)
    polinomio = lab.MPolinomio(coeficientes)
    assert str(polinomio) == "MPolinomio(coefs=[1, 2, 3],grau=2)"
    polinomio = lab.MPolinomio(np.array([1, -2, 0,5,1],dtype=object))
    assert str(polinomio) == "MPolinomio(coefs=[1, -2, 0, 5, 1],grau=4)"
    polinomio = lab.MPolinomio(np.array([-1.3, 3],dtype=object))
    assert str(polinomio) == "MPolinomio(coefs=[-1.3, 3],grau=1)"

def test_unpacking():
    coeficientes = np.array([1, 2, 3])
    polinomio = lab.MPolinomio(coeficientes)
    a, b, c = polinomio
    assert a == 1
    assert b == 2
    assert c == 3




