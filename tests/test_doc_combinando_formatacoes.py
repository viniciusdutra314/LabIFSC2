from LabIFSC2 import *


def test_doc_combinando_formatacoes():
    g=Medida(9.8,'m/s²',0.1)
    print(f"{g:E2}") #(0,098 ± 0,001)x10² m/s²
    print(f"{g:E2_latex}") #(0,098 \, \pm \, 0,001)\times 10^{2} \, \frac{\mathrm{m}}{\mathrm{s}^{2}}
    print(f"{g:cm/s²_E2_latex}") #(9,8 \, \pm \, 0,1)\times 10^{2} \, \frac{\mathrm{cm}}{\mathrm{s}^{2}}
    print(f"{g:E2_cm/s²}") #❌ unidade deve vir primeiro!


    assert f"{g:E2}" == "(0,098 ± 0,001)x10² m/s²"
    assert f"{g:E2_latex}" == r"(0,098 \, \pm \, 0,001)\times 10^{2} \, \frac{\mathrm{m}}{\mathrm{s}^{2}}"
    assert f"{g:cm/s²_E2_latex}" == r"(9,8 \, \pm \, 0,1)\times 10^{2} \, \frac{\mathrm{cm}}{\mathrm{s}^{2}}"