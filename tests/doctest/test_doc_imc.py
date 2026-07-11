from numpy import isclose

from LabIFSC2 import *


def test_doc_imc():
    massa = Medida(75, "kg", 0.1)
    altura = Medida(1.75, "m", 0.01)
    imc = massa / altura**2
    assert str(imc) == "(2,45 ± 0,03)x10¹ kg/m²"
    assert isclose(imc.nominal("kg/m²"), 24.5, rtol=0.01)
    assert isclose(imc.incerteza("kg/m²"), 0.28, rtol=0.01)
    assert isclose(imc.incerteza("si"), 0.28, rtol=0.01)
