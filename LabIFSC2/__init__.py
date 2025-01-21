'''
LabIFSC2
=====
Biblioteca usada pela graduação do IFSC para os laboratórios de física.
Documentação completa em https://viniciusdutra314.github.io/LabIFSC2/
'''


from ._arrays import (arrayM, curva_max, curva_min, incertezas, linspaceM,
                      nominais)
from ._medida import Comparacao, Medida, comparar_medidas, montecarlo
from ._regressões import (MExponencial, MPolinomio, regressao_exponencial,
                          regressao_linear, regressao_polinomial,
                          regressao_potencia)
from .constantes import constantes
