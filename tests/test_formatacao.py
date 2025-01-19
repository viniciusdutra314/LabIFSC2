import LabIFSC2 as lab


def test_arredondamento_da_apostila():
    x=lab.Medida(5.34481349,0.03253496,'m')
    assert str(x)=='(5,34 ± 0,03) m'
    assert str(-x)=='(-5,34 ± 0,03) m'
    assert f"{x:latex}" == r"(5,34 \, \pm \, 0,03) \, \mathrm{m}"
    assert f"{-x:latex}" == r"(-5,34 \, \pm \, 0,03) \, \mathrm{m}"
    x=lab.Medida(5.34481349,0.00363496,'m')
    assert str(x) == '(5,345 ± 0,004) m'
    assert str(-x) == '(-5,345 ± 0,004) m'
    assert f"{x:latex}" == r"(5,345 \, \pm \, 0,004) \, \mathrm{m}"
    assert f"{-x:latex}" == r"(-5,345 \, \pm \, 0,004) \, \mathrm{m}"

def test_arredondamento():
    x=lab.Medida(1.79,0.01,'m')
    assert str(x)=='(1,79 ± 0,01) m'
    assert str(-x)=='(-1,79 ± 0,01) m'
    assert f"{x:latex}" == r"(1,79 \, \pm \, 0,01) \, \mathrm{m}"
    assert f"{-x:latex}" == r"(-1,79 \, \pm \, 0,01) \, \mathrm{m}"

    x._converter_para('cm')
    assert str(x)=='(1,79 ± 0,01)x10² cm'
    assert str(-x)=='(-1,79 ± 0,01)x10² cm'
    assert f"{x:E0}"=='(179 ± 1) cm'
    assert f"{-x:E0}"=='(-179 ± 1) cm'
    g=lab.Medida(981.13413,1.5739275,'cm/s²')
    g._converter_para('m/s²')
    assert str(g)=='(9,81 ± 0,02) m/s²'
    assert str(-g)=='(-9,81 ± 0,02) m/s²'
    
def test_exato():
    x=lab.constantes.speed_of_light_in_vacuum
    assert str(x)=='2,99792458x10⁸ m/s'
    assert str(-x)=='-2,99792458x10⁸ m/s'
    assert f"{x:E0}"=='299792458 m/s'
    assert f"{-x:E0}"=='-299792458 m/s'
    assert f"{x:E0_latex}"==r"299792458 \, \frac{\mathrm{m}}{\mathrm{s}}"
    assert f"{-x:E0_latex}"==r"-299792458 \, \frac{\mathrm{m}}{\mathrm{s}}"
    assert f"{x:latex}"==r"2,99792458\times 10^{8} \, \frac{\mathrm{m}}{\mathrm{s}}"
    assert f"{-x:latex}"==r"-2,99792458\times 10^{8} \, \frac{\mathrm{m}}{\mathrm{s}}"

def test_constantes():
    G=lab.constantes.Newtonian_constant_of_gravitation
    assert str(G)=='(6,6743 ± 0,0001)x10⁻¹¹ m³/kg/s²'
    assert str(-G)=='(-6,6743 ± 0,0001)x10⁻¹¹ m³/kg/s²'
    assert f"{G:latex}"==r"(6,6743 \, \pm \, 0,0001)\times 10^{-11} \, \frac{\mathrm{m}^{3}}{\left(\mathrm{kg} \cdot \mathrm{s}^{2}\right)}"
    assert f"{-G:latex}"==r"(-6,6743 \, \pm \, 0,0001)\times 10^{-11} \, \frac{\mathrm{m}^{3}}{\left(\mathrm{kg} \cdot \mathrm{s}^{2}\right)}"