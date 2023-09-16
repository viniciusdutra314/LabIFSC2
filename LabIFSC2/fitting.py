import numpy as np
from numpy.polynomial import Polynomial

from .medida import Medida



def regressao_polinomial(x:list,y:list,grau : int =1):
    coeficientes, covarianca=np.polyfit(x,y,grau,cov=True)
    erros=np.sqrt(np.diag(covarianca))
    coeficientes_medidas=np.empty(len(coeficientes),dtype=Medida)
    for j in range(len(coeficientes)):
        coeficientes_medidas[j]=Medida(coeficientes[j],erros[j])
    return coeficientes_medidas[::-1]

def regressao_linear(x:list,y:list,grau:int):
    return regressao_linear(x,y,grau)
