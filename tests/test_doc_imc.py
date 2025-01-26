from LabIFSC2 import *


def test_doc_imc():
    massa = Medida(75, 'kg', 0.1)
    altura = Medida(1.75, 'm', 0.01)
    imc = massa / altura**2
    print(imc)  # (2,45 ± 0,03)x10¹ kg/m²
    print(imc.nominal('kg/m²'))  # 24.5
    print(imc.incerteza('kg/m²'))  # 0.3
    print(imc.incerteza('si'))  # 0.3

    assert abs(imc.nominal('kg/m²') - 24.5) < 1e-1
    assert abs(imc.incerteza('kg/m²') - 0.28) < 1e-1
    assert abs(imc.incerteza('si') - 0.28) < 1e-1
