from .matematica import *
from .medida import Medida, montecarlo,equivalente
from .fitting import MPolinomio, regressao_polinomial,regressao_linear, regressao_exponencial
from .arrayM import Nominais, Incertezas, CurvaMin, CurvaMax


__all__=["Medida","montecarlo","equivalente"]+funcoes_matematicas+[
        "MPolinomio","regressao_polinomial","regressao_linear","regressao_exponencial"
        ] + ["Nominais","Incertezas","CurvaMin","CurvaMax"]