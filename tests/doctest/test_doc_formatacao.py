import LabIFSC2 as lab


def test_doc_formatacao() -> None:
    # fmt: off
    # --8<-- [start:formatacao]
    comprimento_de_onda = lab.Medida(500, "nm", 1)
    assert str(comprimento_de_onda) == "(5,00 ± 0,01)x10² nm"
    assert f"{comprimento_de_onda:E0}" == "(500 ± 1) nm"
    assert f"{comprimento_de_onda:E3}" == "(0,500 ± 0,001)x10³ nm"
    massa = lab.Medida(5, "tons", 0.1)
    assert f"{massa:E-1}" == "(50 ± 1)x10⁻¹ ton"
    # --8<-- [end:formatacao]
    # fmt: on
