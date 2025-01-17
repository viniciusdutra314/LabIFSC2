import string
from collections.abc import Iterator
from numbers import Real
from typing import Any

import numpy as np
from numpy.polynomial import Polynomial

from ._matematica import aceitamedida, exp, log, power
from ._medida import Medida
from ._operacoes_em_arrays import arrayM, nominais
from ._tipagem_forte import obrigar_tipos


class MPolinomio:
    @obrigar_tipos
    def __init__(self,coeficientes:np.ndarray):
        if not (isinstance(coeficientes[0],Medida)):
            raise TypeError('Os valores do array não são Medidas')
    
        self._coeficientes:list[Medida]=[]
        for index,coef in enumerate(coeficientes):
            self._coeficientes.append(coef)
            setattr(self,string.ascii_lowercase[index],coef)
        self._grau=len(coeficientes)-1
    
    @obrigar_tipos
    def __call__(self,x:Medida | np.ndarray) -> Medida | np.ndarray:
        avaliar=lambda x:sum(coef*x**(self._grau-i) for i,coef in enumerate(self._coeficientes))
        resultado: Medida | np.ndarray=np.frompyfunc(avaliar,1,1)(x)
        return resultado
    
    def __iter__(self) -> Iterator[Medida]:
        return iter(self._coeficientes)
    def __repr__(self) -> str:
        return f"MPolinomio(coefs={self._coeficientes},grau={self._grau})"



class MExponencial:
    '''Classe para modelar uma função exponencial
    y = a * base^(kx)
    '''
    __slots__ = ['a', 'k', 'base','_valores']
    @obrigar_tipos
    def __init__(self,a:Medida,k:Medida,base:Real):
        self.a=a
        self.base=base
        self.k=k
        self._valores=(a,k,base)

    @obrigar_tipos
    def __call__(self,x:Medida | np.ndarray) -> Medida | np.ndarray:
        resultado:  Medida | np.ndarray=power(float(self.base),x*self.k)
        return resultado
    
    def __repr__(self)->str:
        return f'MExponencial(a={self.a},k={self.k},base={self.base})'
    def __iter__(self)->Iterator[object]:
        return iter(self._valores)

class MLeiDePotencia:
    '''Classe para modelar uma função de lei de potência
    y = a * x^n
    '''
    __slots__ = ['a', 'n','_valores']

    @obrigar_tipos
    def __init__(self, a: Medida, n: Medida):
        self.a = a
        self.n = n
        self._valores = (a, n)
    
    @obrigar_tipos
    def __call__(self, x:Medida | np.ndarray) -> Medida | np.ndarray:
        resultado : Medida | np.ndarray=self.a *power(x, self.n)
        return resultado
    
    def __repr__(self)->str:
        return f'MLeiDePotencia(a={self.a}, b={self.n})'

    def __iter__(self)->Iterator[object]:
        return iter(self._valores)
    
@obrigar_tipos
def regressao_polinomial(x_medidas:np.ndarray,y_medidas:np.ndarray,grau:int) -> MPolinomio:
    if len(x_medidas)!=len(y_medidas):
        raise ValueError("x_dados e y_dados não tem o mesmo tamanho")
    if len(x_medidas)<=grau+1:
        raise ValueError("Não há dados suficientes para um polinômio de grau {grau} (overfitting)")
    if not (isinstance(x_medidas[0],Medida) and isinstance(y_medidas[0],Medida)):
        raise TypeError('x_medidas e y_medidas precisam ser np.ndarray de medidas')
    x_medidas=nominais(x_medidas)
    y_medidas=nominais(y_medidas)
    p, cov = np.polyfit(x_medidas.astype(float), y_medidas.astype(float), grau, cov=True)
    medidas_coeficientes = np.array([Medida(valor, np.sqrt(cov[i, i]),'') for i, valor in enumerate(p)],dtype=Medida)
    return MPolinomio(medidas_coeficientes)

@obrigar_tipos
def regressao_linear(x_medidas:np.ndarray,
                     y_medidas:np.ndarray) -> MPolinomio:
    reta:MPolinomio=regressao_polinomial(x_medidas,y_medidas,1)
    return reta

@obrigar_tipos
def regressao_exponencial(x_medidas:np.ndarray,y_medidas:np.ndarray,
                          base:Real=np.exp(1)) -> MExponencial:
 
    if not np.all(nominais(y_medidas)>0):
            raise ValueError('Todos y precisam ser positivos para uma modelagem exponencial') 

    if base<1: raise ValueError('Base precisa ser maior que 1')
    
    polinomio=regressao_linear(x_medidas,log(y_medidas)/log(base))
    k=polinomio.a
    a=exp(polinomio.b)
    return MExponencial(a,k,base)

@obrigar_tipos
def regressao_potencia(x_medidas:np.ndarray, y_medidas:np.ndarray) -> MLeiDePotencia:
    
    if not bool(np.all(nominais(y_medidas)>0) and np.all(nominais(x_medidas)>0)):
            raise ValueError('Todos x e y precisam ser positivos para uma modelagem exponencial')
    polinomio=regressao_linear(log(x_medidas),log(y_medidas))
    a=exp(polinomio.b)
    n=polinomio.a
    return MLeiDePotencia(a,n)