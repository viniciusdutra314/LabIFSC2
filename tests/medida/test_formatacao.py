import LabIFSC2 as lab


def test_arredondamento_da_apostila() -> None:
    x = lab.Medida(5.34481349, "m", 0.03253496)
    assert x.fmt() == "(5,34 ± 0,03) m"
    assert (-x).fmt() == "(-5,34 ± 0,03) m"
    assert x.fmt(latex=True) == r"(5,34 \, \pm \, 0,03) \, \mathrm{m}"
    assert (-x).fmt(latex=True) == r"(-5,34 \, \pm \, 0,03) \, \mathrm{m}"
    x = lab.Medida(5.34481349, "m", 0.00363496)
    assert x.fmt() == "(5,345 ± 0,004) m"
    assert (-x).fmt() == "(-5,345 ± 0,004) m"
    assert x.fmt(latex=True) == r"(5,345 \, \pm \, 0,004) \, \mathrm{m}"
    assert (-x).fmt(latex=True) == r"(-5,345 \, \pm \, 0,004) \, \mathrm{m}"


def test_arredondamento() -> None:
    x = lab.Medida(1.79, "m", 0.01)
    assert x.fmt() == "(1,79 ± 0,01) m"
    assert (-x).fmt() == "(-1,79 ± 0,01) m"
    assert x.fmt(latex=True) == r"(1,79 \, \pm \, 0,01) \, \mathrm{m}"
    assert (-x).fmt(latex=True) == r"(-1,79 \, \pm \, 0,01) \, \mathrm{m}"

    assert x.fmt(unidade="cm") == "(1,79 ± 0,01) × 10² cm"
    assert (-x).fmt(unidade="cm") == "(-1,79 ± 0,01) × 10² cm"
    assert x.fmt(unidade="cm", expoente=0) == "(179 ± 1) cm"
    assert (-x).fmt(unidade="cm", expoente=0) == "(-179 ± 1) cm"
    g = lab.Medida(981.13413, "cm/s²", 1.5739275)
    assert g.fmt(unidade="m/s²") == "(9,81 ± 0,02) m/s²"
    assert (-g).fmt(unidade="m/s²") == "(-9,81 ± 0,02) m/s²"


def test_exato() -> None:
    x = lab.constantes.speed_of_light_in_vacuum
    assert x.fmt() == "2,99792458 × 10⁸ m/s"
    assert (-x).fmt() == "-2,99792458 × 10⁸ m/s"
    assert x.fmt(expoente=0) == "299792458 m/s"
    assert (-x).fmt(expoente=0) == "-299792458 m/s"
    assert x.fmt(expoente=0, latex=True) == (
        r"299792458 \, \frac{\mathrm{m}}{\mathrm{s}}"
    )
    assert (-x).fmt(expoente=0, latex=True) == (
        r"-299792458 \, \frac{\mathrm{m}}{\mathrm{s}}"
    )
    assert x.fmt(latex=True) == (
        r"2,99792458\times 10^{8} \, \frac{\mathrm{m}}{\mathrm{s}}"
    )
    assert (-x).fmt(latex=True) == (
        r"-2,99792458\times 10^{8} \, \frac{\mathrm{m}}{\mathrm{s}}"
    )


def test_constantes() -> None:
    G = lab.constantes.Newtonian_constant_of_gravitation
    assert G.fmt() == "(6,6743 ± 0,0002) × 10⁻¹¹ m³/kg/s²"
    assert (-G).fmt() == "(-6,6743 ± 0,0002) × 10⁻¹¹ m³/kg/s²"
    assert (
        G.fmt(latex=True) == r"(6,6743 \, \pm \, 0,0002)\times 10^{-11} \, "
        r"\frac{\mathrm{m}^{3}}{\left(\mathrm{kg} \cdot \mathrm{s}^{2}\right)}"
    )
    assert (
        (-G).fmt(latex=True) == r"(-6,6743 \, \pm \, 0,0002)\times 10^{-11} \, "
        r"\frac{\mathrm{m}^{3}}{\left(\mathrm{kg} \cdot \mathrm{s}^{2}\right)}"
    )
