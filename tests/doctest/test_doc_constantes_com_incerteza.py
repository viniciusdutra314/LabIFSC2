import LabIFSC2 as lab


def test_doc_constantes_com_incerteza() -> None:
    mu_0 = lab.constantes.vacuum_mag_permeability
    # fmt: off
    # --8<-- [start:constante_inexata]
    N = 100
    comprimento = lab.Medida(30, "cm", 0.1)
    corrente = lab.Medida(2, "A", 0.01)
    B = mu_0 * N * corrente / comprimento
    assert f"{B:mTesla}" == "(8,38 ± 0,05)x10⁻¹ mT"
    # --8<-- [end:constante_inexata]
    # fmt: on
