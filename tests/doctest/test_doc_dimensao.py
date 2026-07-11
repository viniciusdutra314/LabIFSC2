import LabIFSC2 as lab


def test_doc_dimensao() -> None:
    velocidade = lab.Medida(10, "m/s", 0.1)
    assert str(velocidade.dimensao) == "[length] / [time]"
