import LabIFSC2 as lab
import pytest 

def test_initialization():
    coeficientes = [1, 2, 3]
    polinomio = lab.MPolinomio(coeficientes)
    assert polinomio._coeficientes == coeficientes
    assert polinomio._grau == 2
    assert polinomio.a == 1
    assert polinomio.b == 2
    assert polinomio.c == 3

def test_call():
    coeficientes = [1, 2, 3]
    polinomio = lab.MPolinomio(coeficientes)
    assert polinomio(0) == 3
    assert polinomio(1) == 6
    assert polinomio(2) == 11

def test_str():
    coeficientes = [1, 2, 3]
    polinomio = lab.MPolinomio(coeficientes)
    assert str(polinomio) == "MPolinomio(coefs=[1, 2, 3],grau=2)"
    polinomio = lab.MPolinomio([1, -2, 0,5,1])
    assert str(polinomio) == "MPolinomio(coefs=[1, -2, 0, 5, 1],grau=4)"
    polinomio = lab.MPolinomio([-1.3, 3])
    assert str(polinomio) == "MPolinomio(coefs=[-1.3, 3],grau=1)"

def test_unpacking():
    coeficientes = [1, 2, 3]
    polinomio = lab.MPolinomio(coeficientes)
    a, b, c = polinomio
    assert a == 1
    assert b == 2
    assert c == 3




