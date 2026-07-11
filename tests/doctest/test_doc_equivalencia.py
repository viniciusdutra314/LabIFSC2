import LabIFSC2 as lab


def test_doc_comparar() -> None:
    # fmt: off
    # --8<-- [start:comparacao]
    imc1 = lab.Medida(25, "kg/m²", 0.1)
    imc2 = lab.Medida(24.5, "kg/m²", 0.3)
    assert lab.comparar_medidas(imc1, imc2) == lab.Comparacao.EQUIVALENTES
    # --8<-- [end:comparacao]
    # fmt: on
