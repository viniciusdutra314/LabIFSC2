import LabIFSC2 as lab


def test_doc_combinando_formatacoes() -> None:
    # fmt: off
    # --8<-- [start:formatacoes_combinadas]
    g = lab.Medida(9.8, "m/s²", 0.1)
    assert g.fmt(expoente=2) == "(0,098 ± 0,001) × 10² m/s²"
    assert g.fmt(expoente=2, latex=True) == r"(0,098 \, \pm \, 0,001)\times 10^{2} \, \frac{\mathrm{m}}{\mathrm{s}^{2}}"
    assert g.fmt(unidade="cm/s²", expoente=2, latex=True) == r"(9,8 \, \pm \, 0,1)\times 10^{2} \, \frac{\mathrm{cm}}{\mathrm{s}^{2}}"
    # --8<-- [end:formatacoes_combinadas]
    # fmt: on
