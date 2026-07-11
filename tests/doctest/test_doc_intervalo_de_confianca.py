from numpy import isclose

import LabIFSC2 as lab


def test_doc_intervalo_de_confianca() -> None:
    # fmt: off
    # --8<-- [start:intervalo_confianca]
    imc = lab.Medida(24.5, "kg/m²", 0.3)
    a, b = imc.intervalo_de_confiança(0.95, "kg/m²")
    assert isclose(a, 23.91, rtol=0.01)
    assert isclose(b, 25.08, rtol=0.01)
    # --8<-- [end:intervalo_confianca]
    # fmt: on
