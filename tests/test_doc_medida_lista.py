import pytest

from LabIFSC2 import *


def test_doc_medida_lista():
    diametro=Medida([1.76,1.80,1.77,1.78],'cm',0.005)
    print(diametro) #(1,78 ± 0,01) cm
    diametro_incerteza_grande=Medida([1.76,1.80,1.77,1.78],'cm',0.1)
    print(diametro_incerteza_grande)#(1,8 ± 0,1) cm

    with pytest.raises(ValueError):
        Medida([1.76],'cm',0.005)
    with pytest.raises(ValueError):
        Medida([],'cm',0.005)
    Medida([1.64,153],'cm',0.005)
    assert str(diametro)=="(1,78 ± 0,01) cm"
    assert str(diametro_incerteza_grande)=="(1,8 ± 0,1) cm"