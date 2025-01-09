from pint import UnitRegistry
ureg = UnitRegistry()

from .operacoes_em_arrays import (curva_max, curva_min, get_incertezas, get_nominais,
                     linspace, medida_from_array,)
from .regressões import (MPolinomio, regressao_exponencial, regressao_linear,
                      regressao_polinomial, regressao_potencia,)
from .formatações import *
from .matematica import *
from .medida import Medida, comparar_medidas, montecarlo,Comparacao
from .constantes import *