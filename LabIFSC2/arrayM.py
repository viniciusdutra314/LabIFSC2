import numpy as np
from .medida import Medida

def Nominais(arrayM : iter):
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
            array_nominais[index]=medida

def Incertezas(arrayM : iter):
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
            array_incertezas[index]=medida