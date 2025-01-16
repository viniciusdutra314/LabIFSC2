from numbers import Real
from typing import Any

import numpy as np

from ._medida import Medida
from ._tipagem_forte import obrigar_tipos


@obrigar_tipos
def nominais(arrayMedidas : np.ndarray[Medida,Any]) -> np.ndarray[float,Any]:
    '''*get_nominais* Transforma um array/lista (Sequência) de medidas  em
    um arrays somente com seus valores nominais
    
    Args:
        arrayMedidas (Sequence | np.ndarray): array com medidas

    Returns:
        arrayNominais (Sequence | np.ndarray): array valores nominais

    Raises:
        ValueError: Se algum valor não for uma Medida
  
    Examples:
        >>> import LabIFSC2 as lab
        >>> import numpy as np
        >>> array = np.array([lab.Medida(4, 0.2),lab.Medida(35, 3), lab.Medida(-97, 1)])
        >>> lab.get_nominais(array)
        array([  4.,  35., -97.])
    '''
    return np.array([medida.nominal for medida in arrayMedidas],dtype=float)

@obrigar_tipos
def incertezas(arrayMedidas : np.ndarray[Medida,Any]) -> np.ndarray[float,Any]:
    '''*get_incertezas* Transforma um array/lista (Sequência) de medidas  em
    um arrays somente com suas incertezas
    
    Args:
        arrayMedidas (Sequence[Medida]): array com medidas

    Returns:
        arrayIncertezas(np.ndarray[Medida])  : array com incertezas

    Examples:
        >>> import LabIFSC2 as lab
        >>> import numpy as np
        >>> array = np.array([lab.Medida(4, 0.2),lab.Medida(35, 3), lab.Medida(-97, 1)])
        >>> lab.get_incertezas(array)
        array([0.2, 3. , 1. ])
'''
    return np.array([medida.incerteza for medida in arrayMedidas],dtype=float)

@obrigar_tipos
def curva_min(arrayMedida : np.ndarray[Medida,Any],sigma:float | int =2) -> np.ndarray[float,Any]:
    '''Usada para auxiliar o plot de curvas teóricas
    com erros, com quantidade de sigmas usados personalizável

       curva_min=lab.get_nominais(arrayM) - sigmas*lab.get_incertezas(arrayM)
    
    Args: 
        arrayMedida (Sequence): iterável com Medidas
        sigma (Number): confiança estatística 

    Returns:
        arrayCurva (np.ndarray): array com a curva de Medidas

    '''
    result:np.ndarray[float,Any]=nominais(arrayMedida) -sigma*incertezas(arrayMedida)
    return result

@obrigar_tipos
def curva_max(arrayMedida : np.ndarray[Medida,Any],sigma:float | int=2)-> np.ndarray[float,Any]:
    '''Usada para auxiliar o plot de curvas teóricas
    com erros, quantidade de sigmas usados personalizável

       CurvaMin=Nominais(arrayM) + sigmas*Incertezas(arrayM)

    
    Args: 
        arrayM (Sequence[Medida]) (array,lista,...) com Medidas
        sigma (Number, default=2) relacionada com a confiança estatística 

    Returns:
        arrayCurva (np.ndarray[Medida]): array com a curva de Medidas
    '''
    result:np.ndarray[float,Any]=nominais(arrayMedida) +sigma*incertezas(arrayMedida)
    return result


@obrigar_tipos
def linspace(a:Real,b:Real,n : int,
             incertezas : Real ,unidade : str) -> np.ndarray[Medida,Any]:
    """Gera um array com N Medidas de valor nominal [a,b]
    A incerteza será constante caso 'incertezas' for um número,
    mas se ela for um array cada Medida terá a respectiva incerteza.
    A unidade será a mesma e é opcional
    
    Args:
        `a` (Number): Menor nominal
        `b` (Number): Maior nominal
        `n` (int): Número de Medidas
        `incertezas` (Number | Sequence[Number]): incerteza ou array de incertezas
        `unidade` (str): unidade das medidas
    
    Returns:
        arrayM (np.ndarray[Medida]): array de Medidas

    Examples:
        >>> import LabIFSC2 as lab
        >>> import numpy as np
        >>> a=1 ; b=5 ; N=3
        >>> tempo=lab.linspace(a,b,N,0.1,'s')
        >>> tempo 
        array([(1.0±0.1)s, (3.0±0.1)s, (5.0±0.1)s], dtype=object)
        >>> tempo**2 
        (1.0±0.2)s... (4.0±0.4)s ... (25±1)s]    
    
    Esse é um exemplo com poucos pontos para que
    seja possível observar uma diferença significativa
    entre as Medidas
        
    """
    return np.array([Medida(i,incertezas,unidade) for i in np.linspace(float(a),float(b),n)])
        

@obrigar_tipos
def arrayM(nominais:np.ndarray[Real,Any],incerteza:Real,unidade:str) ->np.ndarray[Medida,Any]:
    '''Converte um array de números em um array de Medidas
    
    Args:
        nominais (Sequence[Number]):  valores nominais
        incerteza (Number): incerteza associada a cada medição 
        unidade (str):  unidade das medições        

    Returns:
        arrayM (np.ndarray[Medida]):  array de Medidas

    '''
    return np.array([Medida(nominal,incerteza,unidade) for nominal in nominais],dtype=Medida)

@obrigar_tipos
def converter_array(arrayM:np.ndarray[Medida,Any],unidade:str)->None:
    for medida in arrayM: medida.converter_para(unidade)
    return None

@obrigar_tipos
def converter_array_si(arrayM:np.ndarray[Medida,Any])->None:
    for medida in arrayM: medida.converter_para_si()
    return None
