from .arrayM import (curva_max, curva_min, get_incertezas, get_nominais,
                     linspace, medida_from_array,)
from .fitting import (MPolinomio, regressao_exponencial, regressao_linear,
                      regressao_polinomial, regressao_potencia,)
from .formatacoes import *
from .lista_de_unidades import *
from .matematica import *
from .medida import Medida, comparar_medidas, montecarlo,Comparacao
from .sistema_de_unidades import TODAS_UNIDADES, Unidade

__all__=["Medida","montecarlo","comparar_medidas","Comparacao"]+funcoes_matematicas+[
        "MPolinomio","regressao_polinomial","regressao_linear","regressao_exponencial","regressao_potencia"
        ] + ["get_nominais","get_incertezas","curva_min","curva_max",
             "linspace","medida_from_array"]+[
            "TODAS_UNIDADES","Unidade"
        ]

np.linspace