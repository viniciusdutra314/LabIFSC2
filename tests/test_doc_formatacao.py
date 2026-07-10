from LabIFSC2 import *


def test_doc_formatacao():
    comprimento_de_onda=Medida(500,'nm',1)
    print(comprimento_de_onda)#(5,00 ± 0,01)x10² nm
    print(f"{comprimento_de_onda:E0}") #(500 ± 1) nm
    print(f"{comprimento_de_onda:E3}") #(0,500 ± 0,001)x10³ nm
    massa=Medida(5,'tons',0.1)
    print(f"{massa:E-1}") #(50 ± 1)x10⁻¹ ton

    assert comprimento_de_onda.__str__() == "(5,00 ± 0,01)x10² nm"
    assert f"{comprimento_de_onda:E0}" == "(500 ± 1) nm"
    assert f"{comprimento_de_onda:E3}" == "(0,500 ± 0,001)x10³ nm"
    assert f"{massa:E-1}" == "(50 ± 1)x10⁻¹ ton"
