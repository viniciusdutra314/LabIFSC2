import numpy as np

from LabIFSC2 import *


def test_coef_raizes():
    r1=Medida(1,0.1) ; r2=Medida(-4,0.2)
    r3=Medida(6,1) ; r4=Medida(25,2)
    raizes=[r1,r2,r3,r4]
    polinomio=MPolinomio.coef_pelas_raizes(raizes)
    for raiz in polinomio.raizes():
        assert raiz in raizes

def test_raizes():
    coefs=[Medida(-1,0.02),Medida(-1,0.03),Medida(1,0.15)]
    polinomio=MPolinomio(coefs)
    polinomio(0)==1
    print(polinomio.raizes()[0])
    assert polinomio.raizes()[0] == -0.6180339887498948
    assert polinomio.raizes()[1] == 1.618033988749895


def test_operacoes_polinomios():
    coefs_a=np.array([Medida(3,0.3),Medida(5,0.2),0,Medida(7,0.2)],dtype=Medida)
    coefs_b=np.array([Medida(12,1),Medida(13,0.01),0,Medida(5,0.3)],dtype=Medida)
    polinomio_a=MPolinomio(coefs_a)
    polinomio_b=MPolinomio(coefs_b)
    assert np.array_equal(coefs_a+coefs_b, (polinomio_a+polinomio_b).coef)
    assert np.array_equal(coefs_a-coefs_b, (polinomio_a-polinomio_b).coef)
    assert np.array_equal(-coefs_a+coefs_b, (-polinomio_a+polinomio_b).coef)