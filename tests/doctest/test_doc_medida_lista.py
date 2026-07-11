import LabIFSC2 as lab


def test_doc_medida_lista() -> None:
    # fmt: off
    # --8<-- [start:medida_lista_incerteza]
    # --8<-- [start:medida_lista]
    diametro = lab.Medida([1.76, 1.80, 1.77, 1.78], "cm", 0.005)
    assert str(diametro) == "(1,78 ± 0,02) cm"
    # --8<-- [end:medida_lista]
    diametro_incerteza_grande = lab.Medida([1.76, 1.80, 1.77, 1.78], "cm", 0.1)
    assert str(diametro_incerteza_grande) == "(1,8 ± 0,1) cm"
    # --8<-- [end:medida_lista_incerteza]
    # fmt: on
