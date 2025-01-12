import LabIFSC as lab1
import LabIFSC2 as lab2
from LabIFSC2 import Medida, regressao_polinomial, MPolinomio
import numpy as np
import pytest 

def test_regressao_linear():

    for _ in range(10):
        num=10
        a,b=np.random.normal(0,1,2)
        epsilon=np.random.normal(0,0.01,num)
        x=np.arange(num)
        y=a*x+b+epsilon
        resposta=lab1.linearize(x,y)
        
        
        x_dados=lab2.arrayM(x,0.01,'s')
        y_dados=lab2.arrayM(y,0.01,'m')
        reta=lab2.regressao_linear(x_dados,y_dados)
        a,b=reta
        print(a.nominal,resposta['a'])
        print(b.nominal,resposta['b'])
        assert np.isclose(a.nominal,resposta['a'],rtol=1e-3)
        assert np.isclose(b.nominal,resposta['b'],rtol=1e-3)
        print(a.incerteza,resposta['Δa'])
        print(b.incerteza,resposta['Δb'])
        assert np.isclose(a.incerteza,resposta['Δa'],rtol=1e-3)
        assert np.isclose(b.incerteza,resposta['Δb'],rtol=1e-3)
def test_regressao_polinominal():
    num=10
    a,b=np.random.normal(0,1,2)
    epsilon=np.random.normal(0,0.001,num)
    x=np.arange(num)
    y=a*x+b+epsilon

    x_dados=lab2.arrayM(x,0.01,'s')
    y_dados=lab2.arrayM(y,0.01,'m')
    parabola=lab2.regressao_polinomial(x_dados,y_dados,2)
    parabola_predito,a_predito,b_predito=parabola
    assert np.isclose(parabola_predito.nominal,0,atol=1e-2)
    assert np.isclose(a_predito.nominal,a,rtol=1e-3)
    assert np.isclose(b_predito.nominal,b,rtol=1e-3)

def test_regressao_polinomial_basic():
    x_dados = np.array([1, 2, 3, 4, 5])
    y_dados = np.array([1, 4, 9, 16, 25])
    grau = 2
    polinomio = regressao_polinomial(x_dados, y_dados, grau)
    assert isinstance(polinomio, MPolinomio)
    assert polinomio._grau == grau

def test_regressao_polinomial_medida():
    x_dados = np.array([Medida(1, 0.1, ''), Medida(2, 0.1, ''), Medida(3, 0.1, ''), Medida(4, 0.1, ''), Medida(5, 0.1, '')])
    y_dados = np.array([Medida(1, 0.1, ''), Medida(4, 0.1, ''), Medida(9, 0.1, ''), Medida(16, 0.1, ''), Medida(25, 0.1, '')])
    grau = 2
    polinomio = regressao_polinomial(x_dados, y_dados, grau)
    assert isinstance(polinomio, MPolinomio)
    assert polinomio._grau == grau

def test_regressao_polinomial_mismatched_lengths():
    x_dados = np.array([1, 2, 3])
    y_dados = np.array([1, 4, 9, 16])
    grau = 2
    with pytest.raises(ValueError, match="x_dados e y_dados não tem o mesmo tamanho"):
        regressao_polinomial(x_dados, y_dados, grau)

def test_regressao_polinomial_insufficient_data():
    x_dados = np.array([1, 2])
    y_dados = np.array([1, 4])
    grau = 1
    with pytest.raises(ValueError):
        regressao_polinomial(x_dados, y_dados, grau)

