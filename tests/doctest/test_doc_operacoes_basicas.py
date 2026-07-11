from LabIFSC2 import *


def test_doc_operacoes_basicas() -> None:

    x = Medida(1, "m", 0.01)
    y = Medida(200, "cm", 1)
    # Operações básicas
    assert str(x + y) == "(3,00 ± 0,01) m"
    assert str(x - y) == "(-1,00 ± 0,01) m"
    assert str(x * y) == "(2,00 ± 0,02) m²"
    assert str(x / y) == "(5,00 ± 0,06)x10⁻¹ "
    assert str(y**2) == "(4,00 ± 0,04)x10⁴ cm²"

    from numpy import isclose

    assert isclose((x + y).nominal("m"), 3, 1e-2)
    assert isclose((x - y).nominal("m"), -1, 1e-2)
    assert isclose((x * y).nominal("m²"), 2, 1e-2)
    assert isclose((x / y).nominal(""), 0.5, 1e-2)
    assert isclose((y**2).nominal("cm²"), 4e4, 1e-2)
