import numpy as np
from .medida import Medida

def get_nominais(arrayMedidas : iter) -> np.ndarray:
    '''Transforma um array/lista (iterável) de medidas  em
    um arrays somente com seus valores nominais
    
    Args:
        arrayMedidas: array com medidas

    Returns:
        arrayNominais  : array valores nominais    
    '''
    try: iter(arrayMedidas)
    except: raise TypeError("A entrada precisa ser um iterable de Medidas")
    tamanho=len(arrayMedidas)
    array_nominais=np.zeros(tamanho)
    
    for index,valores in enumerate(arrayMedidas):
        if not isinstance(valores,Medida):
            valores=Medida(valores)
        array_nominais[index]=valores.nominal
    return array_nominais


def get_incertezas(arrayMedidas : iter) -> np.ndarray:
    '''Transforma um array/lista (iterável) de medidas  em
    um arrays somente com suas incertezas
    
    Args:
        arrayMedidas: array com medidas

    Returns:
        arrayIncertezas  : array com incertezas'''

    try: iter(arrayMedidas)
    except: raise TypeError("A entrada precisa ser um iterable de Medidas")

    tamanho=len(arrayMedidas)
    array_incertezas=np.zeros(tamanho)

    for index,medida in enumerate(arrayMedidas):
        if not isinstance(medida,Medida):
            raise TypeError("Todos os valores precisam ser Medidas")
        else:
            array_incertezas[index]=medida.incerteza
    return array_incertezas


def curva_min(arrayMedida : iter,sigma=2):
    '''Usada para auxiliar o plot de curvas teóricas
    com erros, com quantidade de sigmas usados personalizável

       curva_min=lab.get_nominais(arrayM) - sigmas*lab.get_incertezas(arrayM)
    
    Args: 
        arrayMedida : iterable (array,lista,...) com Medidas
        sigma: confiança estatística 
    '''
    return get_nominais(arrayMedida) -sigma*get_incertezas(arrayMedida)

def curva_max(arrayMedida : iter,sigma=2):
    '''Usada para auxiliar o plot de curvas teóricas
    com erros, quantidade de sigmas usados personalizável

       CurvaMin=Nominais(arrayM) + sigmas*Incertezas(arrayM)

    
    Args: 
        arrayM : iterable (array,lista,...) com Medidas
        sigma (default=2), relacionada com a confiança estatística 
    '''
    return get_nominais(arrayMedida) + sigma*get_incertezas(arrayMedida)


def linspace(a,b,n : int,incertezas,unidade=False) -> np.ndarray[Medida]:
    """Gera um array com N Medidas de valor nominal [a,b]
    A incerteza será constante caso 'incertezas' for um número,
    mas se ela for um array cada Medida terá a respectiva incerteza.
    A unidade será a mesma e é opcional
    
    Args:
        a : Menor nominal
        b : Maior nominal
        n : (int) Número de Medidas
        incertezas : (float | iterable) incerteza ou array de incertezas
        unidade : (str) unidade das medidas
    
    Returns:
        arrayM : array de Medidas
    """
    n=int(n)
    nominais=np.linspace(a,b,n)
    if not hasattr(incertezas,'__iter__'):
        return np.array([Medida(i,incertezas,unidade) for i in nominais])
    if len(incertezas)!=len(nominais):
        raise ValueError('Número de incertezas incompatível com número de nominais')
    else:
        return np.array([Medida(i,j,unidade) for i,j in zip(nominais,incertezas)])
