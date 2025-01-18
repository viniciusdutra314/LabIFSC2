import LabIFSC2 as lab


def test_arredondamento_da_apostila():
    x=lab.Medida(5.34481349,0.03253496,'m')
    assert str(x)=='(5,34 ± 0,03) m'
    assert f"{x:latex}" == "(5,34 \, \pm  \, 0,03) \, m"
    x=lab.Medida(5.34481349,0.00363496,'m')
    assert str(x) == '(5,345 ± 0,004) m'
    assert f"{x:latex}" == "(5,345 \, \pm  \, 0,004) \, m"

def test_arredondamento_da_apostila():
     x=lab.Medida(1.79,0.01,'m')
     assert str(x)=='(1,79 ± 0,01) m'
     assert f"{x:latex}" == "(1,79 \, \pm  \, 0,01) \, m"

     x.converter_para('cm')
     assert str(x)=='(1.79 ± 0.01) 10² cm'
     assert f"{x:latex}" == "(1,79 \, \pm  \, 0,01) \times 10^{2} \, cm" 
     assert f"{x:E0}" == '(1.79 ± 0.01) cm'
     assert f"{x:E0_latex}" == "(179 \, \pm  \, 1) \, cm" 