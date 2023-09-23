from LabIFSC2 import *
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn")
def test_linear_coef():
    x=np.arange(0,30)
    for _ in range(10):
        beta, alpha=np.random.random(2)
        y=alpha*x*(1+0.2*np.random.random(30)) +beta
        b,a=regressao_linear(x,y)
        assert (np.isclose(a.nominal,alpha,rtol=0.3) or a==alpha) and (np.isclose(b.nominal,beta,rtol=0.3) or b==beta)
        plt.scatter(x,y)
        plt.plot(x,x*a + b,color='r')
def test_linear_callable():
    x=np.arange(0,30)
    for _ in range(10):
        beta,alpha=np.random.random(2)
        y=alpha*x*(1+0.7*np.random.random(30)) +beta
        linha=regressao_linear(x,y,func=True)
        plt.scatter(x,y)
        plt.plot(x,linha(x))
        plt.fill_between(x,CurvaMin(linha(x)),CurvaMax(linha(x)),alpha=0.3)
        #plt.show()


def test_polinomio_coef():
    x=np.linspace(-3,3,100)
    d=np.arange(1,10)
    for degree in d:
        for _ in range(10):
            real_coefs=np.random.random(degree+1)-0.5
            y=MPolinomio(real_coefs)(x)
            coefs=regressao_polinomial(x,y,degree)
            for index, coef in enumerate(coefs):
                assert (coef.nominal==real_coefs[index] or np.isclose(coef.nominal,real_coefs[index],rtol=0.6))
            plt.scatter(x,y,alpha=0.5)
            plt.plot(x,MPolinomio(coefs)(x),color='r')

def test_polinomio_callable():
    x=np.linspace(-3,3,100)
    d=np.arange(1,10)
    for degree in d:
        for _ in range(10):
            real_coefs=np.random.random(degree+1)-0.5
            y=MPolinomio(real_coefs)(x)
            polinomio=regressao_polinomial(x,y,degree,func=True)
            coefs=polinomio.coef
            for index, coef in enumerate(coefs):
                assert (coef.nominal==real_coefs[index] or np.isclose(coef.nominal,real_coefs[index],rtol=0.6))
            plt.scatter(x,y,alpha=0.5)
            plt.plot(x,polinomio(x),color='r')
            #plt.show()

#def test_exponencial_coef():


#def test_exponencial_callable():