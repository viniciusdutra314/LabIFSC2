from collections.abc import Sequence
from numbers import Real
from typing import Any

import numpy as np

from ._medida import Medida
from ._tipagem_forte import obrigar_tipos


@obrigar_tipos
def nominais(arrayMedidas : np.ndarray,unidade:str) -> np.ndarray:
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
    if not (isinstance(arrayMedidas[0],Medida)):
        raise TypeError('Os valores do array não são Medidas')
    if unidade=='si':
        return np.array([medida._nominal.to_base_units().magnitude for medida in arrayMedidas],dtype=float)
    else:
        return np.array([medida._nominal.to(unidade).magnitude for medida in arrayMedidas],dtype=float)

@obrigar_tipos
def incertezas(arrayMedidas : np.ndarray,unidade:str) -> np.ndarray:
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
    if not (isinstance(arrayMedidas[0],Medida)):
        raise TypeError('Os valores do array não são Medidas')
    if unidade=='si':
        return np.array([medida._incerteza.to_base_units().magnitude for medida in arrayMedidas],dtype=float)
    else:
        return np.array([medida._incerteza.to(unidade).magnitude for medida in arrayMedidas],dtype=float)


@obrigar_tipos
def linspaceM(a:Real,b:Real,n : int,
             unidade : str,incertezas : Real ,) -> np.ndarray:
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
    return np.array([Medida(i,incertezas,unidade) for i in np.linspace(float(a),float(b),n)],dtype=object)
        

@obrigar_tipos
def arrayM(nominais:np.ndarray | Sequence ,unidade:str,incerteza:Real) ->np.ndarray:
    '''Converte um array de números em um array de Medidas
    
    Args:
        nominais (Sequence[Number]):  valores nominais
        incerteza (Number): incerteza associada a cada medição 
        unidade (str):  unidade das medições        

    Returns:
        arrayM (np.ndarray[Medida]):  array de Medidas

    '''
    if not (isinstance(nominais[0],Real)):
        raise TypeError('Os valores do array não são números reais')

    return np.array([Medida(nominal,incerteza,unidade) for nominal in nominais],dtype=Medida)


