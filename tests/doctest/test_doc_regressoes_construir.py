from LabIFSC2 import *


def test_doc_regressoes_construir() -> None:

    tempos = linspaceM(0, 5, 10, "s", 0.01)
    alturas = arrayM([0, 1.4, 6, 13, 24, 36, 52, 70, 95, 120], "m", 0.1)
    # y=y0 + vt + 1/2gt²
    parabola = regressao_polinomial(tempos, alturas, grau=2)
    a, b, c = parabola  # é possível fazer unpacking dos coeficientes
    assert str(2 * a) == "(9,9 ± 0,3) m/s²"
    assert f"{b:E0}" == "(-0,8 ± 0,7) m/s"
    assert f"{c:E0}" == "(0,4 ± 0,7) m"
    assert str(parabola(Medida(10, "s"))) == "(4,9 ± 0,1)x10² m"

    tempos = linspaceM(0, 10, 11, "year", 0)
    massa = arrayM(
        [
            1,
            4.7e-1,
            2.3e-1,
            1.2e-1,
            6.23e-2,
            3.11e-2,
            1.53e-2,
            7.8e-3,
            4e-3,
            2e-3,
            1e-3,
        ],
        "kg",
        0,
    )
    exponencial = regressao_exponencial(tempos, massa, base=2)
    M_0 = exponencial.amplitude
    meia_vida = -1 / exponencial.expoente
    assert f"{M_0:E0}" == "(0,95 ± 0,01) kg"
    assert f"{meia_vida:a_E0}" == "(1,011 ± 0,004) a"
    assert str(exponencial(Medida(3.5, "year"))) == "(2,98 ± 0,06)x10⁻² kg"
