import LabIFSC2 as lab


def test_doc_imc_cm() -> None:

    massa = lab.Medida(75, "kg", 0.1)
    altura = lab.Medida(175, "cm", 1)
    imc = massa / (altura**2)
    assert imc.fmt() == "(2,45 ± 0,03) × 10⁻³ kg/cm²"
    # fmt: off
    # --8<-- [start:imc_unidades]
    assert imc.fmt() == "(2,45 ± 0,03) × 10⁻³ kg/cm²"
    assert imc.fmt(unidade="kg/m²") == "(2,45 ± 0,03) × 10 kg/m²"
    assert imc.fmt(unidade="g/cm²") == "(2,45 ± 0,03) g/cm²"
    assert imc.fmt(unidade="si") == "(2,45 ± 0,03) × 10 kg/m²"
    # --8<-- [end:imc_unidades]
    # fmt: on
