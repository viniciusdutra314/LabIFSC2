import pint
import pytest

from LabIFSC2 import *

campo_magnético=arrayM([210,90,70,54,39,32,33,27,22,20],'muT',1)
distancias=linspaceM(1,10,10,'cm',0.01) 
unidade_errada=linspaceM(1,10,10,'kg',0.001)

def test_regressao_linear_unidades():
    linha=regressao_linear(distancias,campo_magnético) 
    
    
    linha.amostrar(distancias,'muT')
    distancias_unidade_errada=linspaceM(1,10,10,'',0.001)
    with pytest.raises(ValueError):
       linha.amostrar(distancias_unidade_errada,'muT')
    with pytest.raises(ValueError):
       linha.amostrar(distancias,'kg')
    
    comparar_medidas(linha.amostrar(distancias,'muT',retornar_como_medidas=True)[0],campo_magnético[0])
 
def test_regressao_cubica_unidades():
    for grau in [1,2,3,4,5,6]:
        cubica=regressao_polinomial(distancias,campo_magnético,grau) 
        cubica.amostrar(distancias,'muT')
        with pytest.raises(ValueError):
            cubica.amostrar(unidade_errada,'muT')
        comparar_medidas(cubica.amostrar(distancias,'muT',retornar_como_medidas=True)[0],campo_magnético[0])


def test_regressao_exponencial_unidades():
    exponencial=regressao_exponencial(distancias,campo_magnético) 
    exponencial.amostrar(distancias,'muT')
    with pytest.raises(pint.errors.DimensionalityError):
       exponencial.amostrar(unidade_errada,'muT')
    comparar_medidas(exponencial.amostrar(distancias,'muT',retornar_como_medidas=True)[0],campo_magnético[0])

def test_regressao_potencia_unidades():
    potencia=regressao_potencia(distancias,campo_magnético) 
    potencia.amostrar(distancias,'muT')
    with pytest.raises(ValueError):
       potencia.amostrar(unidade_errada,'muT')
    comparar_medidas(potencia.amostrar(distancias,'muT',retornar_como_medidas=True)[0],campo_magnético[0])
