import LabIFSC2 as lab


def test_doc_incerteza() -> None:
    # fmt: off
    # --8<-- [start:incertezas]
    campo_magnético = lab.arrayM([250, 150, 110, 90, 70, 60, 55, 40, 25, 20], "muT", 1)
    assert str(lab.incertezas(campo_magnético, "muT")) == "[1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]"
    # --8<-- [end:incertezas]
    # fmt: on
