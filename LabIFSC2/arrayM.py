import numpy as np
from .medida import Medida

def Nominais(arrayM : iter) -> np.ndarray:
    '''Transforma um array/lista de medidas, em
    um arrays somente com seus valores nominais'''
    try: iter(arrayM)
    except: raise TypeError("A entrada precisa ser um iterable de Medidas")
    tamanho=len(arrayM)
    array_nominais=np.zeros(tamanho)
    
    for index,medida in enumerate(arrayM):
        if not isinstance(medida,Medida):
            raise TypeError("Todos os valores precisam ser Medidas")
        else:
            array_nominais[index]=medida.nominal
    return array_nominais
def Incertezas(arrayM : iter) -> np.ndarray:
    '''Transforma um array/lista/iterable de medidas, em
    um arrays somente com suas incertezas'''
    try: iter(arrayM)
    except: raise TypeError("A entrada precisa ser um iterable de Medidas")

    tamanho=len(arrayM)
    array_incertezas=np.zeros(tamanho)

    for index,medida in enumerate(arrayM):
        if not isinstance(medida,Medida):
            raise TypeError("Todos os valores precisam ser Medidas")
        else:
            array_incertezas[index]=medida.incerteza
    return array_incertezas


def CurvaMin(arrayM : iter,sigmas=2):
    '''Usada para auxiliar o plot de curvas téoricas
    com erros, quantidade de sigmas usados personalizavel

       CurvaMin=Nominais(arrayM) - sigmas*Incertezas(arrayM)

    
    Args: 
        arrayM : iterable (array,lista,...) com Medidas
        sigma (default=2), relacionada com a confiança estátistica 
    '''
    return Nominais(arrayM) -sigmas*Incertezas(arrayM)

def CurvaMax(arrayM : iter,sigmas=2):
    '''Usada para auxiliar o plot de curvas téoricas
    com erros, quantidade de sigmas usados personalizavel

       CurvaMin=Nominais(arrayM) + sigmas*Incertezas(arrayM)

    
    Args: 
        arrayM : iterable (array,lista,...) com Medidas
        sigma (default=2), relacionada com a confiança estátistica 
    '''
    return Nominais(arrayM) + sigmas*Incertezas(arrayM)
