'''
LabIFSC2
=====
Biblioteca usada pela graduação do IFSC para os laboratórios de física.
Documentação completa em https://viniciusdutra314.github.io/LabIFSC2/
'''


from ._medida import (Medida, comparar_medidas, montecarlo,Comparacao)
from .constantes import constantes
from ._matematica import (aceitamedida, sin, seno, cos, tan, tg, arcsin, asin, arcseno,
    arccos, acos, arctan, atan, arctg, log, ln, log2, log10,
    sinh, senh, cosh, tanh, tgh, arcsinh, asinh, asenh, arccosh,
    acosh, arctanh, atanh, atgh, exp, exp2, sqrt, cbrt, power, pow)

from ._operacoes_em_arrays import (nominais,incertezas,curva_min,
                                  curva_max,linspace,medida_from_array,
                                  arrayM,converter_array,converter_array_si)
from ._regressões import (MPolinomio,MExponencial,regressao_polinomial,regressao_linear,
                         regressao_exponencial,regressao_potencia)






