import re
import numpy as np
from .unidades import Unidade

def arredondar_incerteza(incerteza:float) -> str:
    ''' Transforma um float de incerteza em
    uma string formatada com 1 algarismo 
    significativo 

    Examples:

    >>> arredondar_incerteza(0.314)
    '0.3'
    >>> arredondar_incerteza(0.614)
    '1'
    >>> arredondar_incerteza(3.1e-4)
    '0.0003'
    '''
    power=int(np.log10(incerteza))
    texto=str(incerteza)
    padrao=re.compile('[^+0.,]')
    first_nonzero_position=re.search(padrao,texto).start()
    if int(texto[first_nonzero_position])>5:
        return str(10**power)
    elif first_nonzero_position==0:
        return str(float(texto[0])*10**power)
    else:
        return texto[:first_nonzero_position+1]

def arredondar_nominal(nominal : float,incerteza:float) -> str:
    ''' Recebe um nominal e uma incerteza e retorna
    uma string com o valor nominal formatado em relação
    a incerteza (mesma quantidade de algarismos significativos)

    Examples:
        >>> arredondar_nominal(3,0.1)
        '3.0'
        >>> arredondar_nominal(135.921,0.034)
        '135.92'
        >>> arredondar_nominal(-99,1)
        '-99'
        >>> arredondar_nominal(135,10)
        '130'
        >>> arredondar_nominal(1350,1000)
        '1000'
    '''
    from math import floor
    grandeza_incerteza=floor(np.log10(incerteza))
    if grandeza_incerteza<0:
        return f"{nominal:.{-grandeza_incerteza}f}"
    else:
        nominal=(nominal//10**grandeza_incerteza)*10**grandeza_incerteza
        return str(nominal)


def formatar_medida_console(nominal,incerteza,unidade,
                            ordem_de_grandeza):
    if ordem_de_grandeza:
        if incerteza:
            template='({} ± {})E{} {}'
            return template.format(nominal,incerteza,
                                ordem_de_grandeza,unidade.simbolo).rstrip()
        else:
            template='({})E{} {}'
            return template.format(nominal,ordem_de_grandeza,
                                   unidade.simbolo).rstrip()
    else:
        if incerteza:
            template='({} ± {}) {}'
            return template.format(nominal,incerteza,unidade.simbolo).rstrip()
        else:
            template='({}) {}'
            return template.format(nominal,unidade.simbolo).rstrip()


def formatar_medida_latex(nominal,incerteza,
                          unidade,ordem_de_grandeza):
    if ordem_de_grandeza:
        template=r"({} \pm {}) \times 10^{} \, \text{{{}}}"
        return template.format(nominal,incerteza,
                               ordem_de_grandeza,unidade.simbolo).rstrip()
    else:
        template=r"({} \pm {})\, \text{{{}}}"
        return template.format(nominal,incerteza,unidade.simbolo).rstrip()