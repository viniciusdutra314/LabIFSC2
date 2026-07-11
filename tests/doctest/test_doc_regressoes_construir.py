import LabIFSC2 as lab


def test_doc_regressoes_construir() -> None:
    # fmt: off
    # --8<-- [start:regressao_polinomial]
    tempos = lab.linspaceM(0, 5, 10, "s", 0.01)
    alturas = lab.arrayM([0, 1.4, 6, 13, 24, 36, 52, 70, 95, 120], "m", 0.1)
    # y=y0 + vt + 1/2gt²
    parabola = lab.regressao_polinomial(tempos, alturas, grau=2)
    a, b, c = parabola  # é possível fazer unpacking dos coeficientes
    assert str(2 * a) == "(9,9 ± 0,3) m/s²"
    assert f"{b:E0}" == "(-0,8 ± 0,7) m/s"
    assert f"{c:E0}" == "(0,4 ± 0,7) m"
    assert str(parabola(lab.Medida(10, "s"))) == "(4,9 ± 0,1)x10² m"
    # --8<-- [end:regressao_polinomial]
    # fmt: on

    # fmt: off
    # --8<-- [start:regressao_exponencial]
    tempos = lab.linspaceM(0, 10, 11, "year", 0)
    massa = lab.arrayM([1,0.47,0.23, 0.12, 0.0623, 0.0311,
    0.0153, 0.0078, 0.004, 0.002, 0.001],"kg",0)
    exponencial = lab.regressao_exponencial(tempos, massa, base=2)
    M_0 = exponencial.amplitude
    meia_vida = -1 / exponencial.expoente
    assert f"{M_0:E0}" == "(0,95 ± 0,01) kg"
    assert f"{meia_vida:a_E0}" == "(1,011 ± 0,004) a"
    assert str(exponencial(lab.Medida(3.5, "year"))) == "(2,98 ± 0,06)x10⁻² kg"
    # --8<-- [end:regressao_exponencial]
    # fmt: on
