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


@obrigar_tipos
def _aplicar_funcao_sem_passar_pelo_sistema_de_unidades(
        array_medidas:np.ndarray,lab_func:Callable)->np.ndarray:
    '''
    precisamos aplicar log/exp sem passar pelo sistema de unidades
    um método meio quicky and dirty mas necessário para não dar erro de dimensão
    '''
    medidas_novas=[]
    for medida in array_medidas:
        unidade=str(medida._nominal.units)
        medida_intermediaria=Medida(medida._nominal.magnitude,"",medida._incerteza._magnitude)
        medida_intermediaria=lab_func(medida_intermediaria)
        nominal=medida_intermediaria._nominal._magnitude
        incerteza=medida_intermediaria._incerteza._magnitude
        if np.isnan(nominal) or np.isnan(incerteza):
            raise ValueError(f'Erro ao aplicar {lab_func} no processo de regressão. Lembre-se que, para regressões \
exponenciais, todos os valores de y precisam ser positivos. No caso da regressão de lei de potência, os valores \
em x também precisam ser positivos. Além disso, um valor pode não ser negativo, mas devido à incerteza associada, ele pode assumir valores negativos.')
        medidas_novas.append(Medida(nominal,unidade,incerteza))
    return np.array(medidas_novas)
@obrigar_tipos
def _forcar_troca_de_unidade(array_medidas:np.ndarray,unidade:str)-> np.ndarray:
    return np.array([Medida(med._nominal.magnitude,unidade,med._incerteza.magnitude,) for med in array_medidas])

class ABCRegressao(ABC):
    
    def __init__(self)->None:
        self._amostragem_pre_calculada_nominal: np.ndarray = np.array([])
        self._amostragem_pre_calculada_incerteza: np.ndarray = np.array([])
        self._valores: Iterator = iter([])
        self._sigmas:float=2
    
    def _retornar(self,y:np.ndarray|Medida,unidade_y:str,retornar_como_medidas:bool=False)->np.ndarray|Medida:
        if isinstance(y,Medida): y=np.array([y])
        self._amostragem_pre_calculada_nominal=nominais(y,unidade_y)
        self._amostragem_pre_calculada_incerteza=incertezas(y,unidade_y)
        if y.size==1: y=y[0]
        if retornar_como_medidas: return y
        else: return self._amostragem_pre_calculada_nominal
    
    def _verificar_tipo_de_x(self,x:np.ndarray|Medida)->None:
        if isinstance(x,np.ndarray):
            if not isinstance(x[0],Medida):
                raise TypeError("x precisa ser um array de medidas ou uma medida \
mesmo que com incerteza 0, pois precisamos das unidades")
        return None
    
    @abstractmethod
    def __repr__(self)->str:...

    @abstractmethod
    def amostrar(self, x:np.ndarray|Medida,
                 unidade_y:str,retornar_medidas:bool=False) -> np.ndarray|Medida:...

    def __iter__(self)->Iterator[object]:
        return self._valores

    def mudar_intervalo_de_confianca(self,sigmas:float | int)->None:
        self._sigmas=sigmas

    @property
    def curva_min(self)->np.ndarray:
        if not self._amostragem_pre_calculada_nominal.size:
            raise ValueError('É necessário amostrar a regressão antes de calcular a curva min')
        y:np.ndarray=self._amostragem_pre_calculada_nominal-self._sigmas*self._amostragem_pre_calculada_incerteza
        return y
    
    @property
    def curva_max(self)->np.ndarray:
        if not self._amostragem_pre_calculada_incerteza.size:
            raise ValueError('É necessaŕio amostrar a regressão antes de calcular a curva min')
        y:np.ndarray=self._amostragem_pre_calculada_nominal+self._sigmas*self._amostragem_pre_calculada_incerteza
        return y


class MPolinomio(ABCRegressao):
    @obrigar_tipos
    def __init__(self,coeficientes:np.ndarray):
        if not (isinstance(coeficientes[0],Medida)):
            raise TypeError('Os valores do array não são Medidas')
    
        self._coeficientes:list[Medida]=[]
        for index,coef in enumerate(coeficientes):
            self._coeficientes.append(coef)
            setattr(self,string.ascii_lowercase[index],coef)
        self.grau=len(coeficientes)-1
    
    @obrigar_tipos
    def amostrar(self:'MPolinomio', 
                 x:np.ndarray | Medida,unidade_y:str,retornar_como_medidas:bool=False) -> np.ndarray | Medida:
        self._verificar_tipo_de_x(x)
        y=Medida(0,unidade_y,0)
        for index,coef in enumerate(self._coeficientes):y+=coef*x**(self.grau-index)
        return self._retornar(y,unidade_y,retornar_como_medidas)

    def __iter__(self) -> Iterator[Medida]:
        return iter(self._coeficientes)
    
    def __repr__(self) -> str:
        return f"MPolinomio(coefs={self._coeficientes},grau={self.grau})"



class MExponencial(ABCRegressao):
    '''Classe para modelar uma função exponencial
    y = a * base^(kx)
    '''
    __slots__ = ['cte_multiplicativa', 'expoente', 'base','_valores']
    @obrigar_tipos
    def __init__(self,a:Medida,k:Medida,base:Real):
        self.cte_multiplicativa=a
        self.base=base
        self.expoente=k
        self._valores=iter((a,k,base))
    
    @obrigar_tipos
    def amostrar(self:'MExponencial', x:np.ndarray|Medida, unidade_y:str,retornar_como_medidas:bool=False)->np.ndarray|Medida:
        self._verificar_tipo_de_x(x)
        y:np.ndarray|Medida=np.power(float(self.base),(self.expoente*x))*self.cte_multiplicativa
        return self._retornar(y,unidade_y,retornar_como_medidas)
    
    def __repr__(self)->str:
        return f'MExponencial(cte_multiplicativa={self.cte_multiplicativa},expoente={self.expoente},base={self.base})'

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
    def amostrar(self:'MLeiDePotencia',
                  x:np.ndarray|Medida,unidade_y:str,retornar_como_medidas:bool=False) -> np.ndarray|Medida:
        self._verificar_tipo_de_x(x)
        if isinstance(x,Medida):x=np.array([x])
        unidade_expoente=str((x[0]._nominal**self.n._nominal).units)
        x=_forcar_troca_de_unidade(x,'')    
        expoente=x**self.n
        expoente_medida=_forcar_troca_de_unidade(expoente,unidade_expoente)
        y=expoente_medida*self.a
        if not y[0]._nominal.is_compatible_with(self._y_unidade):
            raise ValueError(f'Unidade de x não está correta')
        return self._retornar(y,unidade_y,retornar_como_medidas)
    
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
        medidas_coeficientes.append(Medida(p[index],unidade,erros[index]))
    return MPolinomio(np.array(medidas_coeficientes))

@obrigar_tipos
def regressao_linear(x_medidas:np.ndarray,
                     y_medidas:np.ndarray) -> MPolinomio:
    reta:MPolinomio=regressao_polinomial(x_medidas,y_medidas,1)
    return reta

@obrigar_tipos
def regressao_exponencial(x_medidas:np.ndarray,y_medidas:np.ndarray,
                          base:Real=np.exp(1)) -> MExponencial:
 
    if base<1: raise ValueError('Base precisa ser maior que 1')
    pegar_log=lambda x: log(x)/log(float(base))
    log_y_medidas=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(y_medidas,pegar_log) 
    polinomio=regressao_linear(x_medidas,log_y_medidas)
    k=polinomio.a
    a=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(np.array([polinomio.b]),exp)[0]
    k=_forcar_troca_de_unidade(np.array([k]),str((1/x_medidas[0]._nominal).units))
    a=_forcar_troca_de_unidade(np.array([a]),str(y_medidas[0]._nominal.units))
    return MExponencial(a[0],k[0],base)

@obrigar_tipos
def regressao_potencia(x_medidas:np.ndarray, y_medidas:np.ndarray) -> MLeiDePotencia:
    log_y_medidas=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(y_medidas,log)
    log_x_medidas=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(x_medidas,log)
    polinomio=regressao_linear(log_x_medidas,log_y_medidas)
    a=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(np.array([polinomio.b]),exp)[0]
    n=polinomio.a
    a=_forcar_troca_de_unidade(np.array([a]),str((y_medidas[0]._nominal/x_medidas[0]._nominal**n._nominal.magnitude).units))
    n=_forcar_troca_de_unidade(np.array([n]),"dimensionless")
    return MLeiDePotencia(a[0],n[0],y_medidas[0]._nominal)