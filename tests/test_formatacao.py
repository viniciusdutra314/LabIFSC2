import LabIFSC2 as lab

x=lab.Medida(15,0.1,'m')
def test_padraolatex():
    assert str(x)=="(1.50 ± 0.01)E1 m"
    assert f'{x:latex}'== "(1.50 \\pm 0.01) \\times 10^1 \\, \\text{m}"
def test_mudandobase():
    x=lab.Medida(456,0.3,'nm')
    assert f'{x:latex}' =='(4.560 \\pm 0.003) \\times 10^2 \\, \\text{nm}'
    assert f'{x}' == "(4.560 ± 0.003)E2 nm"

    assert f'{x:latex_E0}' == '(456.0 \\pm 0.3)\\, \\text{nm}'
    assert f'{x:E0}' == "(456.0 ± 0.3) nm"

def test_removeroarredondamento():
    x=lab.Medida(21.53,1,'cm')
    assert f'{x:latex}' == '(2.2 \\pm 0.1) \\times 10^1 \\, \\text{cm}'
    assert str(x) == r"(2.2 ± 0.1)E1 cm"

    assert f'{x:latex_full}' == '(2.153 \\pm 0.1) \\times 10^1 \\, \\text{cm}'
    assert f'{x:full}' == r"(2.153 ± 0.1)E1 cm"

def test_tudo_junto():
    x=lab.Medida(21.53,1,'cm')
    assert f'{x:latex_full_E0}' == r"(21.53 \pm 1.0)\, \text{cm}"
    assert f'{x:E3_full}' == r"(0.02153 ± 0.001)E3 cm"

def test_negativo():
    x=lab.Medida(1e-9,1e-11,'m')
    assert f'{x:E-11}' =='(100.0 ± 1.0)E-11 m'
    assert f'{x:latex_E-11}' =='(100.0 \\pm 1.0) \\times 10^-11 \\, \\text{m}'
def test_sem_incerteza():
    x=lab.Medida(299_792_458,0)
    assert f'{x:E0}'=='(299792458)'
