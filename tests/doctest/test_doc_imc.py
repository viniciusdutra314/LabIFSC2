from numpy import isclose

import LabIFSC2 as lab


def test_doc_imc() -> None:
    # fmt: off
    # --8<-- [start:imc_calculo]
    massa = lab.Medida(75, "kg", 0.1)
    altura = lab.Medida(1.75, "m", 0.01)
    imc = massa / (altura**2)
    assert imc.fmt() == "(2,45 ± 0,03) × 10 kg/m²"
    # --8<-- [end:imc_calculo]

    # --8<-- [start:imc_valores]
    assert isclose(imc.nominal("kg/m²"), 24.5, rtol=0.01)
    assert isclose(imc.incerteza("kg/m²"), 0.28, rtol=0.01)
    assert isclose(imc.incerteza("si"), 0.28, rtol=0.01)
    # --8<-- [end:imc_valores]
    # fmt: on
