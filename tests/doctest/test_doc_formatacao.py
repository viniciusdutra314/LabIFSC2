import LabIFSC2 as lab


def test_doc_formatacao() -> None:
    # fmt: off
    # --8<-- [start:formatacao]
    comprimento_de_onda = lab.Medida(500, "nm", 1)
    assert comprimento_de_onda.fmt() == "(5,00 ± 0,01) × 10² nm"
    assert comprimento_de_onda.fmt(expoente=0) == "(500 ± 1) nm"
    assert comprimento_de_onda.fmt(expoente=3) == "(0,500 ± 0,001) × 10³ nm"
    massa = lab.Medida(5, "tons", 0.1)
    assert massa.fmt(expoente=-1) == "(50 ± 1) × 10⁻¹ ton"
    # --8<-- [end:formatacao]
    # fmt: on
