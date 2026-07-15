def test_doc_constantes() -> None:
    import LabIFSC2 as lab

    # fmt: off
    # --8<-- [start:constantes_exatas]
    c = lab.constantes.speed_of_light_in_vacuum
    UA = lab.constantes.astronomical_unit
    tempo = UA / c
    assert tempo.fmt(unidade="minute") == "8,316746397269274 min"
    # --8<-- [end:constantes_exatas]
    # fmt: on
