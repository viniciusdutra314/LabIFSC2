import string
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from numbers import Real
from typing import Any

import numpy as np
import pint
from numpy import exp, log, power
from numpy.polynomial import Polynomial

from ._arrays import arrayM, incertezas, nominais
from ._medida import Medida, ureg
from ._tipagem_forte import obrigar_tipos


def _aplicar_funcao_sem_passar_pelo_sistema_de_unidades(
        array_medidas:np.ndarray,lab_func:Callable)->np.ndarray:
    '''
    #precisamos aplicar log/exp sem passar pelo sistema de unidades
    #um método meio quicky and dirty mas necessário para não dar erro de dimensão
    '''
    medidas_novas=[]
    for medida in array_medidas:
        unidade=str(medida._nominal.units)
        medida_intermediaria=Medida(medida._nominal.magnitude,medida._incerteza._magnitude,"")
        medida_intermediaria=lab_func(medida_intermediaria)
        nominal=medida_intermediaria._nominal._magnitude
        incerteza=medida_intermediaria._incerteza._magnitude
        medidas_novas.append(Medida(nominal,incerteza,unidade))
    return np.array(medidas_novas)
def _forcar_troca_de_unidade(medida:Medida|np.ndarray,unidade:str)-> Medida | np.ndarray:
    if isinstance(medida,np.ndarray):
        return np.array([Medida(med._nominal.magnitude,med._incerteza.magnitude,unidade) for med in medida])
    else:
        return Medida(medida._nominal.magnitude,medida._incerteza.magnitude,unidade)

class ABCRegressao(ABC):
    
    def __init__(self)->None:
        self._amostragem_pre_calculada_nominal: np.ndarray = np.array([])
        self._amostragem_pre_calculada_incerteza: np.ndarray = np.array([])
        self._valores: Iterator = iter([])
    
    @abstractmethod
    def __repr__(self)->str:...

    @abstractmethod
    def amostrar(self, x:np.ndarray,unidade_x:str,unidade_y:str) -> np.ndarray:...

    def __iter__(self)->Iterator[object]:
        return self._valores

    def curva_min(self,sigmas:float | int=2)->np.ndarray:
        if not isinstance(sigmas,Real):
            raise TypeError('sigmas precisa ser um número real')
        if not self._amostragem_pre_calculada_nominal.size:
            raise ValueError('É necessário amostrar a regressão antes de calcular a curva min')
        return self._amostragem_pre_calculada_nominal-sigmas*self._amostragem_pre_calculada_incerteza
    
    def curva_max(self,sigmas:float | int=2)->np.ndarray:
        if not isinstance(sigmas,Real):
            raise TypeError('sigmas precisa ser um número real')
        if not self._amostragem_pre_calculada_incerteza.size:
            raise ValueError('É necessaŕio amostrar a regressão antes de calcular a curva min')
        return self._amostragem_pre_calculada_nominal+sigmas*self._amostragem_pre_calculada_incerteza



class MPolinomio(ABCRegressao):
    @obrigar_tipos
    def __init__(self,coeficientes:np.ndarray):
        if not (isinstance(coeficientes[0],Medida)):
            raise TypeError('Os valores do array não são Medidas')
    
        self._coeficientes:list[Medida]=[]
        for index,coef in enumerate(coeficientes):
            self._coeficientes.append(coef)
            setattr(self,string.ascii_lowercase[index],coef)
        self._grau=len(coeficientes)-1
    

    def __iter__(self) -> Iterator[Medida]:
        return iter(self._coeficientes)
    
    def __repr__(self) -> str:
        return f"MPolinomio(coefs={self._coeficientes},grau={self._grau})"



class MExponencial(ABCRegressao):
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
    
    def __repr__(self)->str:
        return f'MExponencial(a={self.a},k={self.k},base={self.base})'

class MLeiDePotencia(ABCRegressao):
    '''Classe para modelar uma função de lei de potência
    y = a * x^n
    '''

    @obrigar_tipos
    def __init__(self, a: Medida, n: Medida,y_unidade:pint.Quantity):
        super().__init__()
        self.a = a
        self.n = n
        self._valores=iter([a,n])
        self._y_unidade=y_unidade
    
    @obrigar_tipos
    def amostrar(self, x:np.ndarray,unidade_x:str,unidade_y:str) -> np.ndarray:
        expoente=x**self.n
        expoente_medida=_forcar_troca_de_unidade(expoente,str(ureg(unidade_x)**self.n._nominal))
        y=expoente_medida*self.a
        if isinstance(y,np.ndarray):#essa linha é só para o mpy não reclamar que y não é indexável 
            if not y[0]._nominal.is_compatible_with(self._y_unidade):
                raise ValueError(f'Unidade de x não está correta')
        self._amostragem_pre_calculada_nominal=nominais(y,unidade_y)
        self._amostragem_pre_calculada_incerteza=incertezas(y,unidade_y)
        return self._amostragem_pre_calculada_nominal
    
    def __repr__(self)->str:
        return f'MLeiDePotencia(a={self.a}, b={self.n})'



@obrigar_tipos
def regressao_polinomial(x_medidas:np.ndarray,y_medidas:np.ndarray,grau:int) -> MPolinomio:
    if len(x_medidas)!=len(y_medidas):
        raise ValueError("x_dados e y_dados não tem o mesmo tamanho")
    if len(x_medidas)<=grau+1:
        raise ValueError("Não há dados suficientes para um polinômio de grau {grau} (overfitting)")
    if not (isinstance(x_medidas[0],Medida) and isinstance(y_medidas[0],Medida)):
        raise TypeError('x_medidas e y_medidas precisam ser np.ndarray de medidas')
    x_float=np.array([x._nominal.magnitude for x in x_medidas],dtype=float)
    y_float=np.array([y._nominal.magnitude for y in y_medidas],dtype=float)
    p, cov = np.polyfit(x_float, y_float, grau, cov=True)
    erros=np.sqrt(np.diag(cov))
    medidas_coeficientes=[]
    for index in range(len(p)):
        unidade= str((y_medidas[0]._nominal/x_medidas[0]._nominal**(grau-index)).units)
        medidas_coeficientes.append(Medida(p[index],erros[index],unidade))
    return MPolinomio(np.array(medidas_coeficientes))

@obrigar_tipos
def regressao_linear(x_medidas:np.ndarray,
                     y_medidas:np.ndarray) -> MPolinomio:
    reta:MPolinomio=regressao_polinomial(x_medidas,y_medidas,1)
    return reta

@obrigar_tipos
def regressao_exponencial(x_medidas:np.ndarray,y_medidas:np.ndarray,
                          base:Real=np.exp(1)) -> MExponencial:
 
    if not np.all([y._nominal.magnitude>0 for y in y_medidas]):
            raise ValueError('Todos y precisam ser positivos para uma modelagem exponencial') 

    if base<1: raise ValueError('Base precisa ser maior que 1')
    
    pegar_log=lambda x: log(x)/log(float(base))
    log_y_medidas=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(y_medidas,pegar_log) 
    polinomio=regressao_linear(x_medidas,log_y_medidas)
    k=polinomio.a
    a=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(np.array([polinomio.b]),exp)[0]
    
    k=_forcar_troca_de_unidade(k,str((1/x_medidas[0]._nominal).units))
    a=_forcar_troca_de_unidade(a,str(y_medidas[0]._nominal.units))
    return MExponencial(a,k,base)

@obrigar_tipos
def regressao_potencia(x_medidas:np.ndarray, y_medidas:np.ndarray) -> MLeiDePotencia:
    
    if not bool(np.all([y._nominal.magnitude>0 for y in y_medidas]) and np.all([x._nominal.magnitude>0 for x in x_medidas])):
            raise ValueError('Todos x e y precisam ser positivos para uma modelagem exponencial')
    log_y_medidas=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(y_medidas,log)
    log_x_medidas=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(x_medidas,log)
    polinomio=regressao_linear(log_x_medidas,log_y_medidas)
    a=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(np.array([polinomio.b]),exp)[0]
    n=polinomio.a
    a=_forcar_troca_de_unidade(a,str((y_medidas[0]._nominal/x_medidas[0]._nominal**n._nominal.magnitude).units))
    n=_forcar_troca_de_unidade(n,"dimensionless")
    return MLeiDePotencia(a,n,y_medidas[0]._nominal)