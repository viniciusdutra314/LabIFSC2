import LabIFSC as lab1
import numpy as np
import uncertainties.umath as umath
from uncertainties import ufloat

import LabIFSC2 as lab2

'''
Aqui estamos comparando as bibliotecas LabIFSC, LabIFSC2 e uncertainties 
no regime de erros pequenos, nesse caso, as bibliotecas devem retornar valores próximos
visto que a aproximação linear do LabIFSC/uncertainties vai ser equivalente
ao monte carlo do LabIFSC2.

Usamos alguns números mágicos de precisão, não há respaldo teórico para esses valores,
mas como via de regra quanto mais próximos melhor.

Como o monte carlo é um método estátistico, as vezes os testes não iriam passar por 
pura flutuação estátisticas... Então é interessante a precisão de comparação não 
ser muita alta

'''

def comparar_relativo_ufloat_lab1_lab2(ufloat:ufloat,medida_lab1:lab2.Medida,
                              medida_lab2:lab1.Medida,precisao=1e-3):
    assert np.isclose(medida_lab1.nominal,ufloat.nominal_value,rtol=precisao)
    assert np.isclose(medida_lab1.nominal,medida_lab2.nominal,rtol=precisao)

    assert np.isclose(medida_lab1.incerteza,ufloat.std_dev,rtol=precisao)
    assert np.isclose(medida_lab1.incerteza,medida_lab2.incerteza,rtol=precisao)

def comparar_absoluto_ufloat_lab1_lab2(ufloat:ufloat,medida_lab1:lab2.Medida,
                              medida_lab2:lab1.Medida,precisao=1e-3):
    assert np.isclose(medida_lab1.nominal,ufloat.nominal_value,atol=precisao)
    assert np.isclose(medida_lab1.nominal,medida_lab2.nominal,atol=precisao)

    assert np.isclose(medida_lab1.incerteza,ufloat.std_dev,atol=precisao)
    assert np.isclose(medida_lab1.incerteza,medida_lab2.incerteza,atol=precisao)



def comparar_ufloat_lab2(ufloat:ufloat,medida_lab2:lab2.Medida,precisao=1e-3):
    assert np.isclose(medida_lab2.nominal,ufloat.nominal_value,rtol=precisao)
    assert np.isclose(medida_lab2.incerteza,ufloat.std_dev,rtol=precisao)


def test_number_in_a_lab_func(): assert lab2.sin(0)==0

def test_arithmetic_operations():
    incerteza = 1e-4
    for value1 in np.linspace(10, 2.6, 10):
        for value2 in np.linspace(25, 3, 10):
            x = ufloat(value1, incerteza) + ufloat(value2, incerteza)
            x_lab1 = lab1.Medida((value1, incerteza), '') + lab1.Medida((value2, incerteza), '')
            x_lab2 = lab2.Medida(value1, incerteza, '') + lab2.Medida(value2, incerteza, '')
            comparar_absoluto_ufloat_lab1_lab2(x, x_lab1, x_lab2)

            x = ufloat(value1, incerteza) - ufloat(value2, incerteza)
            x_lab1 = lab1.Medida((value1, incerteza), '') - lab1.Medida((value2, incerteza), '')
            x_lab2 = lab2.Medida(value1, incerteza, '') - lab2.Medida(value2, incerteza, '')
            comparar_absoluto_ufloat_lab1_lab2(x, x_lab1, x_lab2)

            
            x = ufloat(value1, incerteza) * ufloat(value2, incerteza)
            x_lab1 = lab1.Medida((value1, incerteza), '') * lab1.Medida((value2, incerteza), '')
            x_lab2 = lab2.Medida(value1, incerteza, '') * lab2.Medida(value2, incerteza, '')
            comparar_absoluto_ufloat_lab1_lab2(x, x_lab1, x_lab2)

            x = ufloat(value1, incerteza) / ufloat(value2, incerteza)
            x_lab1 = lab1.Medida((value1, incerteza), '') / lab1.Medida((value2, incerteza), '')
            x_lab2 = lab2.Medida(value1, incerteza, '') / lab2.Medida(value2, incerteza, '')
            comparar_absoluto_ufloat_lab1_lab2(x, x_lab1, x_lab2)






def test_trignometria():
    incerteza=1e-6
    for value in np.linspace(0.5,0,9,100):
        x = umath.sin(ufloat(value, incerteza))
        x_lab1 = lab1.sin(lab1.Medida((value, incerteza), ''))
        x_lab2 = lab2.sin(lab2.Medida(value, incerteza, ''))
        comparar_relativo_ufloat_lab1_lab2(x, x_lab1, x_lab2)

        x = umath.cos(ufloat(value, incerteza))
        x_lab1 = lab1.cos(lab1.Medida((value, incerteza), ''))
        x_lab2 = lab2.cos(lab2.Medida(value, incerteza, ''))
        comparar_relativo_ufloat_lab1_lab2(x, x_lab1, x_lab2)

        x = umath.tan(ufloat(value, incerteza))
        x_lab1 = lab1.tan(lab1.Medida((value, incerteza), ''))
        x_lab2 = lab2.tan(lab2.Medida(value, incerteza, ''))
        comparar_relativo_ufloat_lab1_lab2(x, x_lab1, x_lab2, precisao=1e-1)

        x = umath.asin(ufloat(value , incerteza))
        x_lab1 = lab1.arc_sin(lab1.Medida((value , incerteza), ''))
        x_lab2 = lab2.asin(lab2.Medida(value , incerteza, ''))
        comparar_relativo_ufloat_lab1_lab2(x, x_lab1, x_lab2)

        x = umath.acos(ufloat(value , incerteza))
        x_lab1 = lab1.arc_cos(lab1.Medida((value , incerteza), ''))
        x_lab2 = lab2.acos(lab2.Medida(value , incerteza, ''))
        comparar_relativo_ufloat_lab1_lab2(x, x_lab1, x_lab2)

        x = umath.atan(ufloat(value, incerteza))
        x_lab1 = lab1.arc_tan(lab1.Medida((value, incerteza), ''))
        x_lab2 = lab2.atan(lab2.Medida(value, incerteza, ''))
        comparar_relativo_ufloat_lab1_lab2(x, x_lab1, x_lab2,precisao=1)

def test_hiperbolicas():
    incerteza = 1e-6
    for value in np.linspace(0.5, 1, 100):
        x = umath.sinh(ufloat(value, incerteza))
        x_lab2 = lab2.sinh(lab2.Medida(value, incerteza, ''))
        comparar_ufloat_lab2(x, x_lab2,precisao=1e-2)

        x = umath.cosh(ufloat(value, incerteza))
        x_lab2 = lab2.cosh(lab2.Medida(value, incerteza, ''))
        comparar_ufloat_lab2(x, x_lab2)

        x = umath.tanh(ufloat(value, incerteza))
        x_lab2 = lab2.tanh(lab2.Medida(value, incerteza, ''))
        comparar_ufloat_lab2(x, x_lab2)

        x = umath.asinh(ufloat(value, incerteza))
        x_lab2 = lab2.asinh(lab2.Medida(value, incerteza, ''))
        comparar_ufloat_lab2(x, x_lab2)

        x = umath.acosh(ufloat(value + 1, incerteza))  # value + 1 to ensure it's in the domain of acosh
        x_lab2 = lab2.acosh(lab2.Medida(value + 1, incerteza, ''))
        comparar_ufloat_lab2(x, x_lab2)

        x = umath.atanh(ufloat(value / 2, incerteza))  # value / 2 to ensure it's in the domain of atanh
        x_lab2 = lab2.atanh(lab2.Medida(value / 2, incerteza, ''))
        comparar_ufloat_lab2(x, x_lab2)


def test_power():
    incerteza = 1e-8
    for value in np.linspace(1,3,100):
        x = umath.pow(ufloat(value, incerteza), 2)
        x_lab1 = lab1.Medida((value, incerteza), '')**2
        x_lab2 = lab2.pow(lab2.Medida(value, incerteza, ''), 2)
        comparar_relativo_ufloat_lab1_lab2(x, x_lab1, x_lab2)

        x = umath.pow(ufloat(value, incerteza), 3)
        x_lab1 = lab1.Medida((value, incerteza), '')**3
        x_lab2 = lab2.pow(lab2.Medida(value, incerteza, ''), 3)
        comparar_relativo_ufloat_lab1_lab2(x, x_lab1, x_lab2)

        x = umath.sqrt(ufloat(value, incerteza))
        x_lab1 = lab1.sqrt(lab1.Medida((value, incerteza), ''))
        x_lab2 = lab2.sqrt(lab2.Medida(value, incerteza, ''))
        comparar_relativo_ufloat_lab1_lab2(x, x_lab1, x_lab2)

        x = ufloat(value, incerteza)**(1/3)
        x_lab1 = lab1.cbrt(lab1.Medida((value, incerteza), ''))
        x_lab2 = lab2.cbrt(lab2.Medida(value, incerteza, ''))
        comparar_relativo_ufloat_lab1_lab2(x, x_lab1, x_lab2)

