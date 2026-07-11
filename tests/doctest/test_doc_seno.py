import LabIFSC2 as lab


def test_doc_seno_vetorizado() -> None:
    import numpy as np

    theta = lab.Medida(30, "degree", 0.01)
    assert (
        str(np.sin(theta))  # type: ignore[call-overload]
        == "(5,000 ± 0,002)x10⁻¹ "
    )
