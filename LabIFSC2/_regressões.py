import string
from collections.abc import Sequence
from numbers import Number

import numpy as np
from numpy.polynomial import Polynomial
from numpy.typing import NDArray

from ._matematica import aceitamedida, exp, log, power
from ._medida import Medida
from ._operacoes_em_arrays import arrayM, nominais
from ._tipagem_forte import obrigar_tipos


class MPolinomio:
    @obrigar_tipos
    def __init__(self,coeficientes:np.ndarray[Medida] | np.ndarray[Number]):
        self._coeficientes=[]
        for index,coef in enumerate(coeficientes):
            self._coeficientes.append(coef)
            setattr(self,string.ascii_lowercase[index],coef)
        self._grau=len(coeficientes)-1
    
    
    def __call__(self,x):
        avaliar=lambda x:sum(coef*x**(self._grau-i) for i,coef in enumerate(self._coeficientes))
        return np.frompyfunc(avaliar,1,1)(x)
    
    def __iter__(self):
        return iter(self._coeficientes)
    def __repr__(self):
        return f"MPolinomio(coefs={self._coeficientes},grau={self._grau})"



class MExponencial:
    '''Classe para modelar uma função exponencial
    y = a * base^(kx)
    '''
    @obrigar_tipos
    def __init__(self,a:Medida,k:Medida,base:Number):
        self.a=a
        self.base=base
        self.k=k
        self._valores=[a,k,base]

    def __call__(self,x):
        return power(self.base,x*self.k)
    
    def __repr__(self):
        return f'MExponencial(a={self.a},k={self.k},base={self.base})'
    def __iter__(self):
        return iter(self._valores)

class MLeiDePotencia:
    '''Classe para modelar uma função de lei de potência
    y = a * x^b
    '''
    @obrigar_tipos
    def __init__(self, a: Medida, n: Medida):
        self.a = a
        self.n = n

    def __call__(self, x):
        return self.a *power(x, self.n)

    def __repr__(self):
        return f'MLeiDePotencia(a={self.a}, b={self.n})'

    def __iter__(self):
        return iter(self._valores)
    
@obrigar_tipos
def regressao_polinomial(x_dados:np.ndarray[Medida] | np.ndarray[Number],
                         y_dados:np.ndarray[Medida] | np.ndarray[Number],grau:int) -> MPolinomio:
    if len(x_dados)!=len(y_dados):
        raise ValueError("x_dados e y_dados não tem o mesmo tamanho")
    if len(x_dados)<=grau+1:
        raise ValueError("Não há dados suficientes para um polinômio de grau {grau} (overfitting)")

    if isinstance(x_dados[0],Medida): x_dados=nominais(x_dados)
    if isinstance(y_dados[0],Medida): y_dados=nominais(y_dados)
    p, cov = np.polyfit(x_dados.astype(float), y_dados.astype(float), grau, cov=True)
    medidas_coeficientes = np.array([Medida(valor, np.sqrt(cov[i, i]),'') for i, valor in enumerate(p)],dtype=Medida)
    return MPolinomio(medidas_coeficientes)

@obrigar_tipos
def regressao_linear(x:np.ndarray[Medida] | np.ndarray[Number],
                     y:np.ndarray[Medida] | np.ndarray[Number]) -> MPolinomio:

    return regressao_polinomial(x,y,1)

@obrigar_tipos
def regressao_exponencial(x:np.ndarray[Medida] | np.ndarray[Number],
                          y:np.ndarray[Medida] | np.ndarray[Number],
                          base:Number=np.exp(1)) -> MExponencial:

    if isinstance(y,Medida): 
        if not np.all(y.nominal>0):
            raise ValueError('Todos y precisam ser positivos para uma modelagem exponencial')
    else:
        if not np.all(y>0):
            raise ValueError('Todos y precisam ser positivos para uma modelagem exponencial')    

    if base<1: raise ValueError('Base precisa ser maior que 1')
    
    polinomio=regressao_linear(x,log(y)/log(base))
    k=polinomio.a
    a=exp(polinomio.b)
    return MExponencial(a,k,base)

@obrigar_tipos
def regressao_potencia(x:np.ndarray[Medida] | np.ndarray[Number],
                       y:np.ndarray[Medida] | np.ndarray[Number]) -> MExponencial:

    if isinstance(y,Medida): 
        if not np.all(y.nominal>0):
            raise ValueError('Todos y precisam ser positivos para uma modelagem exponencial')
    else:
        if not np.all(y>0):
            raise ValueError('Todos y precisam ser positivos para uma modelagem exponencial')  
    
    if isinstance(x,Medida): 
        if not np.all(x.nominal>0):
            raise ValueError('Todos y precisam ser positivos para uma modelagem exponencial')
    else:
        if not np.all(x>0):
            raise ValueError('Todos y precisam ser positivos para uma modelagem exponencial')  
    


    polinomio=regressao_linear(log(x),log(y))
    a=exp(polinomio.b)
    n=polinomio.a
    return MLeiDePotencia(a,n)