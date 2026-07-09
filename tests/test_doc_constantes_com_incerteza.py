def test_doc_constantes_com_incerteza():
    import LabIFSC2 as lab
    mu_0 = lab.constantes.vacuum_mag_permeability
    N = 100
    L = lab.Medida(30, 'cm', 0.1)
    I = lab.Medida(2, 'A', 0.01)
    B = mu_0 * N * I / L
    print(f"{B:mTesla}")  # (8,38 ± 0,05)x10⁻¹ mT

    assert f"{B:mTesla}" == "(8,38 ± 0,05)x10⁻¹ mT"
