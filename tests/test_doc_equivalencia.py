from LabIFSC2 import *


def test_doc_comparar():
    imc1 = Medida(25, 'kg/m²', 0.1)
    imc2 = Medida(24.5, 'kg/m²', 0.3)
    print(comparar_medidas(imc1, imc2))
    # Comparacao.EQUIVALENTES

    assert comparar_medidas(imc1, imc2) == Comparacao.EQUIVALENTES
