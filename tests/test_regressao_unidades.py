import numpy as np
import pint
import pytest

from LabIFSC2 import *

campo_magnético=arrayM([210,90,70,54,39,32,33,27,22,20],'muT',1)
distancias=linspaceM(1,10,10,'cm',0.01) 
unidade_errada=linspaceM(1,10,10,'kg',0.001)

def test_regressao_linear_unidades():
    linha=regressao_linear(distancias,campo_magnético) 
    
    valores = nominais(linha(distancias), 'muT')
    distancias_unidade_errada=linspaceM(1,10,10,'',0.001)
    with pytest.raises(Exception):
       nominais(linha(distancias_unidade_errada), 'muT')
    with pytest.raises(Exception):
       nominais(linha(distancias), 'kg')
    np.isclose(valores[0],campo_magnético[0].nominal('muT'),rtol=1e-2)
 
def test_regressao_cubica_unidades():
    for grau in [1,2,3,4,5,6]:
        cubica=regressao_polinomial(distancias,campo_magnético,grau) 
        nominais(cubica(distancias), 'muT')
        with pytest.raises(Exception):
            nominais(cubica(unidade_errada), 'muT')
        np.isclose(nominais(cubica(distancias), 'muT')[0],campo_magnético[0].nominal('muT'),rtol=1e-2)


def test_regressao_exponencial_unidades():
    exponencial=regressao_exponencial(distancias,campo_magnético) 
    nominais(exponencial(distancias), 'muT')
    with pytest.raises(Exception):
       nominais(exponencial(unidade_errada), 'muT')
    np.isclose(nominais(exponencial(distancias), 'muT')[0],campo_magnético[0].nominal('muT'),rtol=1e-2)

def test_regressao_potencia_unidades():
    potencia=regressao_potencia(distancias,campo_magnético) 
    nominais(potencia(distancias), 'muT')
    with pytest.raises(Exception):
       nominais(potencia(unidade_errada), 'muT')
    np.isclose(nominais(potencia(distancias), 'muT')[0],campo_magnético[0].nominal('muT'),rtol=1e-2)
