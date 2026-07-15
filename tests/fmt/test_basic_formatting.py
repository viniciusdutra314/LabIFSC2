import pytest

import LabIFSC2 as lab


def test_formatação_sem_incerteza() -> None:
    x = lab.Medida(5, "cm")
    assert x.fmt() == "5 cm"
    assert x.fmt(unidade="m") == "5 × 10⁻² m"
    assert (
        lab.Medida(0.051, "m").fmt(unidade="m", separador_decimal=".") == "5.1 × 10⁻² m"
    )
    assert lab.Medida(0.051, "m").fmt(unidade="m") == "5,1 × 10⁻² m"
    assert lab.Medida(-0.05, "m").fmt() == "-5 × 10⁻² m"
    assert lab.Medida(0, "m").fmt() == "0 m"
    assert x.fmt(unidade="mm") == "5 × 10 mm"
    assert x.fmt(unidade="um") == "5 × 10⁴ µm"
    assert x.fmt(unidade="um", expoente=3) == "50 × 10³ µm"


def test_formatação_rejeita_separador_decimal_inválido() -> None:
    with pytest.raises(ValueError, match="separador decimal"):
        lab.Medida(5, "cm").fmt(separador_decimal=";")  # type: ignore[arg-type]


def test_formatação_com_incerteza() -> None:
    medida = lab.Medida(5.34481349, "m", 0.03253496)

    assert medida.fmt() == "(5,34 ± 0,03) m"
    assert medida.fmt(unidade="cm") == "(5,34 ± 0,03) × 10² cm"
    assert medida.fmt(separador_decimal=".") == "(5.34 ± 0.03) m"
    assert lab.Medida(-0.004, "m", 0.01).fmt(expoente=0) == "(0,00 ± 0,01) m"


def test_formatação_latex() -> None:
    medida = lab.Medida(5.34481349, "m", 0.03253496)

    assert medida.fmt(latex=True) == r"(5,34 \, \pm \, 0,03) \, \mathrm{m}"
    assert lab.Medida(5, "m").fmt(latex=True) == r"5 \, \mathrm{m}"
