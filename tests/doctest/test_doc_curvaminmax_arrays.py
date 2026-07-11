import LabIFSC2 as lab


def test_doc_cuvraminmax_arrays() -> None:
    curva = lab.linspaceM(0, 5, 6, "m", 0.1)
    assert str(lab.curva_min(curva, "m")) == "[-0.2  0.8  1.8  2.8  3.8  4.8]"
    assert str(lab.curva_max(curva, "m")) == "[0.2 1.2 2.2 3.2 4.2 5.2]"

    assert str(lab.curva_min(curva, "m", 4)) == "[-0.4  0.6  1.6  2.6  3.6  4.6]"
    assert str(lab.curva_max(curva, "m", 4)) == "[0.4 1.4 2.4 3.4 4.4 5.4]"
