import numpy as np
from .medida import Medida


def get_nominais(arrayMedidas : iter) -> np.ndarray:
    '''*get_nominais* Transforma um array/lista (iterável) de medidas  em
    um arrays somente com seus valores nominais
    
    Args:
        arrayMedidas: array com medidas

    Returns:
        arrayNominais  : array valores nominais

  
    Examples:
        >>> import LabIFSC2 as lab
        >>> import numpy as np
        >>> array = np.array([lab.Medida(4, 0.2),lab.Medida(35, 3), lab.Medida(-97, 1)])
        >>> lab.get_nominais(array)
        array([  4.,  35., -97.])
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
    '''*get_incertezas* Transforma um array/lista (iterável) de medidas  em
    um arrays somente com suas incertezas
    
    Args:
        arrayMedidas: array com medidas

    Returns:
        arrayIncertezas  : array com incertezas

    Examples:
        >>> import LabIFSC2 as lab
        >>> import numpy as np
        >>> array = np.array([lab.Medida(4, 0.2),lab.Medida(35, 3), lab.Medida(-97, 1)])
        >>> lab.get_incertezas(array)
        array([0.2, 3. , 1. ])
'''
    
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
        arrayMedida (iter): iterável com Medidas
        sigma (float | int): confiança estatística 

    Returns:
        arrayCurva (np.ndarray): array com a curva de Medidas

    '''
    return get_nominais(arrayMedida) -sigma*get_incertezas(arrayMedida)

def curva_max(arrayMedida : iter,sigma=2):
    '''Usada para auxiliar o plot de curvas teóricas
    com erros, quantidade de sigmas usados personalizável

       CurvaMin=Nominais(arrayM) + sigmas*Incertezas(arrayM)

    
    Args: 
        arrayM : iterable (array,lista,...) com Medidas
        sigma (default=2), relacionada com a confiança estatística 

    Returns:
        arrayCurva (np.ndarray): array com a curva de Medidas
    '''
    return get_nominais(arrayMedida) + sigma*get_incertezas(arrayMedida)


def linspace(a:float,b:float,n : int,
             incertezas :float,unidade : str =False) -> np.ndarray[Medida]:
    """Gera um array com N Medidas de valor nominal [a,b]
    A incerteza será constante caso 'incertezas' for um número,
    mas se ela for um array cada Medida terá a respectiva incerteza.
    A unidade será a mesma e é opcional
    
    Args:
        a (float): Menor nominal
        b (float): Maior nominal
        n (int): Número de Medidas
        incertezas (float | iterable): incerteza ou array de incertezas
        unidade (str): unidade das medidas
    
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
    n=int(n)
    nominais=np.linspace(a,b,n)
    if not hasattr(incertezas,'__iter__'):
        return np.array([Medida(i,incertezas,unidade) for i in nominais])
    if len(incertezas)!=len(nominais):
        raise ValueError('Número de incertezas incompatível com número de nominais')
    else:
        return np.array([Medida(i,j,unidade) for i,j in zip(nominais,incertezas)])

def medida_from_array(array:iter,unidade='',incerteza =0) -> Medida:
    ''' 
    Converte um iteravel de medições em um único objeto da
    classe Medida
    
    Args:
        array (iter):  array com medições 
        unidade (str):  unidade das medições 
        incerteza (float): incerteza associada a cada medição 

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
    media=np.average(array) 
    desvio_padrao=np.std(array)
    if incerteza>desvio_padrao:
        desvio_padrao=incerteza
    return Medida(media,desvio_padrao,unidade)

