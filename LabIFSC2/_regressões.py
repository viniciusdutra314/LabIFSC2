import string
from collections.abc import Sequence
from numbers import Number

import numpy as np
from numpy.polynomial import Polynomial
from numpy.typing import NDArray

from ._matematica import aceitamedida, exp
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

    def __call__(self,x:Number|Medida)->Medida|np.ndarray[Medida]:
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
    def __init__(self,a:Medida,k:Medida,base:Number):
        self.a=a
        self.base=base
        self.k=k
        self._valores=[a,k,base]
    def __call__(self,x):
        return self.a*np.power(self.base,self.k*x)
    def __repr__(self):
        return f'MExponencial(a={self.a},k={self.k},base={self.base})'
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
    '''Encontre a melhor reta (minímos quadrados)
    
    y = a * x + b

    Args:
        x , y iterables (arrays,list,...) com floats ou Medidas
    Return : 
        Array com Coeficientes
    '''
    return regressao_polinomial(x,y,1)

@obrigar_tipos
def regressao_exponencial(x,y,base=np.exp(1),func=False):
    '''Encontre a melhor exponencial da forma
    \(y = a * e^{kx}\) para os dados x,y

    É possível mudar a base, por exemplo, 
    base=2 ira encontrar a melhor função

    \(y=a*2^{kx}\)

    Args:
        x (iterable): Medidas ou floats
        y (iterable): Medidas ou floats
        base (float): Base da exponencial
        func (bool): retorna uma função ao invés do fitting
    
    Returns:
        Array (nd.array):  Medidas a , k se func=False
        Função (callable): retorna y(x) se func=True
        
    '''
    if isinstance(y,Medida): 
        if not np.all(y.nominal>0):
            raise ValueError('Todos y precisam ser positivos para uma modelagem exponencial')
    else:
        if not np.all(y>0):
            raise ValueError('Todos y precisam ser positivos para uma modelagem exponencial')    

    if base<1: raise ValueError('Base precisa ser maior que 1')
    
    coefs=regressao_linear(x,np.log(y)/np.log(base))
    coefs[0]=exp(coefs[0])
    
@obrigar_tipos
def regressao_potencia(x, y,func=False) :
    '''Com um conjunto de dados x,y,
    esse método encontra a melhor lei de 
    potência da forma  \(y=A * (x^n)\)

    Args:
        x (iterable): Medidas ou números
        y (iterable): Medidas ou números
        func (bool): Retorna uma função ao invés do fitting
        
    Returns:
        Array (nd.array):  Medidas a , k se func=False
        Função (callable): retorna y(x) se func=True
    '''
    x=nominais(x) ; y=nominais(y)
    coefs=regressao_linear(np.log(x),np.log(y))
    coefs[0]=exp(coefs[0])
    if not func: return coefs
    else: return aceitamedida(lambda x:coefs[0]*x**coefs[1])
