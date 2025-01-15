'''
LabIFSC2
=====
Biblioteca usada pela graduação do IFSC para os laboratórios de física.
Documentação completa em https://viniciusdutra314.github.io/LabIFSC2/
'''


from ._matematica import (aceitamedida, acos, acosh, arccos, arccosh, arcseno,
                          arcsin, arcsinh, arctan, arctanh, arctg, asenh, asin,
                          asinh, atan, atanh, atgh, cbrt, cos, cosh, exp, exp2,
                          ln, log, log2, log10, pow, power, senh, seno, sin,
                          sinh, sqrt, tan, tanh, tg, tgh,)
from ._medida import Comparacao, Medida, comparar_medidas, montecarlo
from ._operacoes_em_arrays import (arrayM, converter_array, converter_array_si,
                                   curva_max, curva_min, incertezas, linspace,
                                   medida_from_array, nominais,)
from ._regressões import (MExponencial, MPolinomio, regressao_exponencial,
                          regressao_linear, regressao_polinomial,
                          regressao_potencia,)
from .constantes import constantes
