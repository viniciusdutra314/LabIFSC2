import LabIFSC2 as lab


def test_doc_nominal() -> None:

    campo_magnético = lab.arrayM([250, 150, 110, 90, 70, 60, 55, 40, 25, 20], "muT", 1)
    assert (
        str(lab.nominais(campo_magnético, "muT"))
        == "[250. 150. 110.  90.  70.  60.  55.  40.  25.  20.]"
    )
