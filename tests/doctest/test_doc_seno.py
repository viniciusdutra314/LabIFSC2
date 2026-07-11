import LabIFSC2 as lab


def test_doc_seno_vetorizado() -> None:
    import numpy as np

    # fmt: off
    # --8<-- [start:seno]
    theta = lab.Medida(30, "degree", 0.01)
    assert str(np.sin(theta))  == "(5,000 ± 0,002)x10⁻¹ "
    # --8<-- [end:seno]
    # fmt: on
