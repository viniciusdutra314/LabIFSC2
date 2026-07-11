import LabIFSC2 as lab


def test_doc_sqrt_vetorizado() -> None:
    import numpy as np

    # fmt: off
    # --8<-- [start:code]
    areas = np.array([lab.Medida(4, "cm²", 0.24),
                      lab.Medida(9, "m²", 0.24),
                      lab.Medida(16, "km²", 0.24)])
    lados = np.sqrt(areas)
    assert str(lados) == "[(2,00 ± 0,06) cm (3,00 ± 0,04) m (4,00 ± 0,03) km]"
    # --8<-- [end:code]
    # fmt: on
