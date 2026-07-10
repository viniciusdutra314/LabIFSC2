from LabIFSC2 import *


def test_doc_dimensao():
    velocidade=Medida(10,'m/s',0.1)
    assert str(velocidade.dimensao) == '[length] / [time]'