from collections.abc import Sequence
from numbers import Real
from typing import Any

import numpy as np

from ._medida import Medida
from ._tipagem_forte import obrigar_tipos


@obrigar_tipos
def nominais(arrayMedidas : np.ndarray,unidade:str) -> np.ndarray:
    """
        Converte um array de objetos Medida para um array de valores nominais em uma unidade especificada.
        
        Args:
            arrayMedidas (np.ndarray): Array de objetos Medida.
            unidade (str): Unidade para a conversão dos valores nominais. Use 'si' para unidades do Sistema Internacional.
        
        Returns:
            np.ndarray: Array de valores nominais convertidos para a unidade especificada.
        
        Raises:
            TypeError: Se algum dos valores no array não for um objeto Medida.
    """
       

    if not (isinstance(arrayMedidas[0],Medida)):
        raise TypeError('Os valores do array não são Medidas')
    if unidade=='si':
        return np.array([medida._nominal.to_base_units().magnitude for medida in arrayMedidas],dtype=float)
    else:
        return np.array([medida._nominal.to(unidade).magnitude for medida in arrayMedidas],dtype=float)

@obrigar_tipos
def incertezas(arrayMedidas : np.ndarray,unidade:str) -> np.ndarray:
    """
        Converte um array de objetos Medida para um array de incertezas em uma unidade especificada.
        
        Args:
            arrayMedidas (np.ndarray): Array de objetos Medida.
            unidade (str): Unidade para a conversão das incertezas. Use 'si' para unidades do Sistema Internacional.
        
        Returns:
            np.ndarray: Array de incertezas convertidas para a unidade especificada.
        
        Raises:
            TypeError: Se algum dos valores no array não for um objeto Medida.
    """

    if not (isinstance(arrayMedidas[0],Medida)):
        raise TypeError('Os valores do array não são Medidas')
    if unidade=='si':
        return np.array([medida._incerteza.to_base_units().magnitude for medida in arrayMedidas],dtype=float)
    else:
        return np.array([medida._incerteza.to(unidade).magnitude for medida in arrayMedidas],dtype=float)


@obrigar_tipos
def linspaceM(a:Real,b:Real,n : int,unidade:str,incertezas:Real) -> np.ndarray:
    """Gera um array de Medidas com valores igualmente espaçados.
    
    Args:
        a (Real): O valor inicial do intervalo.
        b (Real): O valor final do intervalo.
        n (int): O número de elementos no array.
        unidade (str): A unidade das medidas.
        incertezas (Real): A incerteza associada a cada medida.
    
    Returns:
        np.ndarray: Um array de objetos Medida com valores igualmente espaçados.
    """
    return np.array([Medida(i,unidade,incertezas) for i in np.linspace(float(a),float(b),n)],dtype=object)
        

@obrigar_tipos
def arrayM(nominais:np.ndarray | Sequence ,unidade:str,incerteza:Real) ->np.ndarray:
    """
    Cria um array de objetos Medida a partir de valores nominais, unidade e incerteza.
    
    Args:
        nominais (np.ndarray | Sequence): Uma sequência de valores nominais.
        unidade (str): A unidade de medida.
        incerteza (Real): A incerteza associada aos valores nominais.
    
    Returns:
        np.ndarray: Um array de objetos Medida.
    
    Raises:
        TypeError: Se os valores do array não forem números reais.
    """

    if not (isinstance(nominais[0],Real)):
        raise TypeError('Os valores do array não são números reais')

    return np.array([Medida(nominal,unidade,incerteza) for nominal in nominais],dtype=Medida)


