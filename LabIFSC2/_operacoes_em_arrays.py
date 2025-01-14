import numpy as np
from ._medida import Medida
from numbers import Number
from ._tipagem_forte import obrigar_tipos
from collections.abc import Sequence

@obrigar_tipos
def nominais(arrayMedidas : np.ndarray[Medida]) -> np.ndarray[Number]:
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
    tamanho=len(arrayMedidas)
    array_nominais=np.empty(tamanho)
    
    for index,valores in enumerate(arrayMedidas):
        array_nominais[index]=valores.nominal
    return array_nominais

@obrigar_tipos
def incertezas(arrayMedidas : np.ndarray[Medida]) -> np.ndarray[Number]:
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
    
    tamanho=len(arrayMedidas)
    array_incertezas=np.empty(tamanho)
    
    for index,valores in enumerate(arrayMedidas):
        if not isinstance(valores,Medida):
            raise ValueError("Todos os valores precisam ser Medidas")
        array_incertezas[index]=valores.incerteza
    return array_incertezas

@obrigar_tipos
def curva_min(arrayMedida : np.ndarray[Medida],sigma:Number=2) -> np.ndarray[Number]:
    '''Usada para auxiliar o plot de curvas teóricas
    com erros, com quantidade de sigmas usados personalizável

       curva_min=lab.get_nominais(arrayM) - sigmas*lab.get_incertezas(arrayM)
    
    Args: 
        arrayMedida (Sequence): iterável com Medidas
        sigma (Number): confiança estatística 

    Returns:
        arrayCurva (np.ndarray): array com a curva de Medidas

    '''
    return nominais(arrayMedida) -sigma*incertezas(arrayMedida)

@obrigar_tipos
def curva_max(arrayMedida : np.ndarray[Medida],sigma:Number=2)-> np.ndarray[Number]:
    '''Usada para auxiliar o plot de curvas teóricas
    com erros, quantidade de sigmas usados personalizável

       CurvaMin=Nominais(arrayM) + sigmas*Incertezas(arrayM)

    
    Args: 
        arrayM (Sequence[Medida]) (array,lista,...) com Medidas
        sigma (Number, default=2) relacionada com a confiança estatística 

    Returns:
        arrayCurva (np.ndarray[Medida]): array com a curva de Medidas
    '''
    return nominais(arrayMedida) + sigma*incertezas(arrayMedida)


@obrigar_tipos
def linspace(a:Number,b:Number,n : int,
             incertezas : Number ,unidade : str) -> np.ndarray[Medida]:
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
    if a>b: raise ValueError("a é maior do que b")

    nominais=np.linspace(a,b,n)
    return np.array([Medida(i,incertezas,unidade) for i in nominais])
        
@obrigar_tipos
def medida_from_array(medições: np.ndarray[Number],
                      incerteza_experimental:Number,unidade:str) -> Medida:
    ''' 
    Converte uma sequência de medições em um único objeto da
    classe Medida
    
    Args:
        medições (Sequence[Number]):  medições  
        incerteza (Number): incerteza associada a cada medição 
        unidade (str):  unidade das medições        

    Returns:
        medida (Medida):  medida 

    Examples:
        Suponha que você tenha realizado varias medições e queria
        converter elas em somente uma Medida, por exemplo, você mediu
        várias vezes o diamêtro de um fio irregular

        >>> diametro=medida_from_array([1.73,1.76,1.77,1.77,1.83],'mm')
        >>> diametro
        Medida(nominal=1.7719999999999998,incerteza=0.03249615361854387,unidade='mm')
        
        Caso a incerteza de cada medição for maior do que o desvio padrão, 
        o erro será considero a incerteza do experimento

        >>> diametro=medida_from_array([1.73,1.76,1.77,1.77,1.83],'mm',incerteza=0.05)
        >>> diametro
        Medida(nominal=1.7719999999999998,incerteza=0.05,unidade='mm')
    '''
@obrigar_tipos
def arrayM(nominais:np.ndarray[Number],incerteza:Number,unidade:str) ->np.ndarray[Medida]:
    '''Converte um array de números em um array de Medidas
    
    Args:
        nominais (Sequence[Number]):  valores nominais
        incerteza (Number): incerteza associada a cada medição 
        unidade (str):  unidade das medições        

    Returns:
        arrayM (np.ndarray[Medida]):  array de Medidas

    '''
    if isinstance(incerteza,Number):
        return np.array([Medida(nominal,incerteza,unidade) for nominal in nominais])
    else:
        return np.array([Medida(nominal,incerteza,unidade) for nominal,incerteza in zip(nominais,incerteza)])

@obrigar_tipos
def converter_array(arrayM:np.ndarray[Medida],unidade:str)->np.ndarray[Medida]:
    for medida in arrayM: medida.converter_para(unidade)
    return None

@obrigar_tipos
def converter_array_si(arrayM:np.ndarray[Medida])->np.ndarray[Medida]:
    for medida in arrayM: medida.converter_para_si()
    return None
