import LabIFSC2 as lab


def test_doc_operacoes_basicas_arrays() -> None:
    import numpy as np

    # fmt: off
    # --8<-- [start:operacoes_arrays]
    x = np.array([lab.Medida(1, "m", 0.01), lab.Medida(2, "m", 0.01)])
    y = np.array([lab.Medida(200, "cm", 1), lab.Medida(400, "cm", 1)])

    assert str(x + y) == "[(3,00 ± 0,01) m (6,00 ± 0,01) m]"
    assert str(x - y) == "[(-1,00 ± 0,01) m (-2,00 ± 0,01) m]"
    assert str(x * y) == "[(2,00 ± 0,02) m² (8,00 ± 0,04) m²]"
    assert str(x / y) == "[(5,00 ± 0,06) × 10⁻¹ (5,00 ± 0,03) × 10⁻¹]"
    assert str(y**2) == "[(4,00 ± 0,04) × 10⁴ cm² (1,600 ± 0,008) × 10⁵ cm²]"
    # --8<-- [end:operacoes_arrays]
    # fmt: on

    assert np.isclose((x + y)[0].nominal("m"), 3, rtol=1e-3)
    assert np.isclose((x - y)[1].nominal("m"), -2, rtol=1e-3)
    assert np.isclose((x * y)[1].nominal("m²"), 8, rtol=1e-3)
    assert np.isclose((x / y)[1].nominal(""), 5e-1, rtol=1e-3)
    assert np.isclose((y * y)[1].nominal("cm²"), 1.6e5, rtol=1e-3)
