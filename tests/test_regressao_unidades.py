import pint
import pytest

from LabIFSC2 import *

campo_magnético=arrayM([210,90,70,54,39,32,33,27,22,20],1,'muT')
distancias=linspaceM(1,10,10,0.01,'cm') 
unidade_errada=linspaceM(1,10,10,0.001,'kg')

def test_regressao_linear_unidades():
    linha=regressao_linear(distancias,campo_magnético) 
    linha(distancias)
    unidade_errada=linspaceM(1,10,10,0.001,'')
    with pytest.raises(ValueError):
       linha(unidade_errada)
    comparar_medidas(linha(distancias)[0],campo_magnético[0])

def test_regressao_cubica_unidades():
    for grau in [1,2,3,4,5,6]:
        cubica=regressao_polinomial(distancias,campo_magnético,grau) 
        cubica(distancias)
        with pytest.raises(ValueError):
            cubica(unidade_errada)
        comparar_medidas(cubica(distancias)[0],campo_magnético[0])


def test_regressao_exponencial_unidades():
    exponencial=regressao_exponencial(distancias,campo_magnético) 
    exponencial(distancias)
    with pytest.raises(pint.errors.DimensionalityError):
       exponencial(unidade_errada)
    comparar_medidas(exponencial(distancias)[0],campo_magnético[0])

def test_regressao_potencia_unidades():
    potencia=regressao_potencia(distancias,campo_magnético) 
    potencia(distancias)
    with pytest.raises(ValueError):
       potencia(unidade_errada)
    comparar_medidas(potencia(distancias)[0],campo_magnético[0])
