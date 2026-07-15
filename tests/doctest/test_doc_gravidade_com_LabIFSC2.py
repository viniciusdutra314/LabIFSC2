import LabIFSC2 as lab


def test_doc_gravidade_com_LabIFSC2() -> None:
    # fmt: off
    # --8<-- [start:gravidade]
    # g=4π²L/T²
    pi = lab.constantes.pi
    L = lab.Medida(15, "cm", 0.1)
    T = lab.Medida(780, "ms", 1)
    gravidade = (4 * pi**2) * L / T**2
    # --8<-- [start:gravidade_latex]
    assert gravidade.fmt(unidade="si") == "(9,73 ± 0,07) m/s²"
    assert gravidade.fmt(unidade="si", latex=True) == r"(9,73 \, \pm \, 0,07) \, \frac{\mathrm{m}}{\mathrm{s}^{2}}"
    # --8<-- [end:gravidade_latex]
    # --8<-- [end:gravidade]
    # fmt: on
