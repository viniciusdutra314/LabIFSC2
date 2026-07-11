def test_doc_gravidade_sem_labifsc() -> None:
    import math

    # fmt: off
    # --8<-- [start:gravidade_manual]
    # g=4π²L/T²
    # conversões manuais
    L = 15 * 1e-2
    dL = 0.1 * 1e-2
    T = 780 * 1e-3
    dT = 1 * 1e-3
    g = (4 * math.pi**2) * L / (T**2)
    # propagação de erro usando derivada
    dg = (4 * math.pi**2) * (
        math.sqrt(math.pow(dL / T**2, 2) + math.pow(2 * L * dT / T**3, 2))
    )
    assert f"{g:.2f} ± {dg:.2f} m/s²" == "9.73 ± 0.07 m/s²"
    # --8<-- [end:gravidade_manual]
    # fmt: on
