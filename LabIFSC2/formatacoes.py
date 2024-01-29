import re
import numpy as np
from .unidades import Unidade

def formatar_incerteza(incerteza:float) -> str:
    ''' Transforma um float de incerteza em
    uma string formatada com 1 algarismo 
    significativo 

    Examples:

    >>> formatar_incerteza(0.314)
    '0.3'
    >>> formatar_incerteza(0.614)
    '1'
    >>> formatar_incerteza(3.1e-4)
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

def formatar_nominal(nominal : float,incerteza:float) -> str:
    ''' Recebe um nominal e uma incerteza e retorna
    uma string com o valor nominal formatado em relação
    a incerteza (mesma quantidade de algarismos significativos)

    Examples:
        >>> formatar_nominal(3,0.1)
        '3.0'
        >>> formatar_nominal(135.921,0.034)
        '135.92'
        >>> formatar_nominal(-99,1)
        '-99'
        >>> formatar_nominal(135,10)
        '130'
        >>> formatar_nominal(1350,1000)
        '1000'
    '''
    from math import floor
    grandeza_incerteza=floor(np.log10(incerteza))
    if grandeza_incerteza<0:
        return f"{nominal:.{-grandeza_incerteza}f}"
    else:
        nominal=(nominal//10**grandeza_incerteza)*10**grandeza_incerteza
        return str(nominal)

def formatar_medida(nominal,incerteza,ordem_de_grandeza=None):
    if ordem_de_grandeza==None:
        ordem_de_grandeza=int(np.log10(np.abs(nominal)))
    nominal/=10**ordem_de_grandeza
    incerteza/=10**ordem_de_grandeza
    nominal_str=formatar_nominal(nominal,incerteza)
    incerteza_str=formatar_incerteza(incerteza)
    return nominal_str,incerteza_str,ordem_de_grandeza
   
    

def formatar_medida_console(nominal,incerteza,unidade,
                            ordem_de_grandeza=None):
    '''
    Examples:
        >>> import LabIFSC2 as lab
        >>> metro=lab.TODAS_UNIDADES['m']
        >>> formatar_medida_console(15,0.1,metro)
        '(1.50 ± 0.01)E1 m'
        >>> formatar_medida_console(195.13,6,metro)
        '(1.95 ± 0.1)E2 m'
        >>> formatar_medida_console(-3,0.4,metro)
        '(-3.0 ± 0.4) m'
        >>> formatar_medida_console(1e-4,3.14e-6,metro)
        '(1.00 ± 0.03)E-4 m'
        >>> formatar_medida_console(-1e-4,3.14e-6,metro)
        '(-1.00 ± 0.03)E-4 m'
    '''
    nominal_str,incerteza_str,ordem_de_grandeza=formatar_medida(nominal,incerteza,ordem_de_grandeza)
    if ordem_de_grandeza!=0:
        return f'({nominal_str} ± {incerteza_str})E{ordem_de_grandeza} {unidade.simbolo}'
    else:
        return f'({nominal_str} ± {incerteza_str}) {unidade.simbolo}'


def formatar_medida_latex(nominal,incerteza,
                          unidade,ordem_de_grandeza=None):
    '''
    Examples:
        >>> import LabIFSC2 as lab
        >>> metro=lab.TODAS_UNIDADES['m']
        >>> print(formatar_medida_latex(15,0.1,metro))
        (1.50 \pm 0.01) \\times 10^{1} \, \\text{m}

        >>> print(formatar_medida_latex(15,0.1,metro,0))
        (15.0 \pm 0.1)\, \text{m}

        >>> print(formatar_medida_latex(15,0.1,metro,-3))
        (15000.0 \pm 100.0) \times 10^{-3} \, \text{m}
        >>> print(formatar_medida_latex(195.13,6,metro))
        (1.95 \pm 0.1) \\times 10^{2} \, \\text{m}

        >>> print(formatar_medida_latex(-3,0.4,metro))
        (-3.0 \pm 0.4)\, \\text{m}

        >>> print(formatar_medida_latex(1e-4,3.14e-6,metro))
        (1.00 \pm 0.03) \\times 10^{-4} \, \\text{m}

        >>> print(formatar_medida_latex(-1e-4,3.14e-6,metro))
        (-1.00 \pm 0.03) \\times 10^{-4} \, \\text{m}
    '''    
    nominal_str,incerteza_str,ordem_de_grandeza=formatar_medida(nominal,incerteza,ordem_de_grandeza)
    if ordem_de_grandeza!=0:
        resultado=rf"({nominal_str} \pm {incerteza_str}) \times 10^{{{ordem_de_grandeza}}} \, \text{{{unidade.simbolo}}}"
        return resultado
    else:
        return rf'({nominal_str} \pm {incerteza_str})\, \text{{{unidade.simbolo}}}'