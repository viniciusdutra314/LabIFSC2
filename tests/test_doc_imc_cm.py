from LabIFSC2 import *


def test_doc_imc_cm():
    

    massa= Medida(75,0.1,'kg')
    altura= Medida(175,1,'cm')
    imc=massa/altura**2
    print(imc) #(2,45 ± 0,03)x10⁻³ kg/cm²
    print(f"{imc:kg/m²}") #(2,45 ± 0,03)x10¹ kg/m²
    print(f"{imc:g/cm²}") #(2,45 ± 0,03) g/cm²
    print(f"{imc:si}") #(2,45 ± 0,03)x10¹ kg/m²
    print(f"{imc}")
    assert f"{imc:g/cm²}"=="(2,45 ± 0,03) g/cm²"
    assert f"{imc}==(2,45 ± 0,03)x10⁻³ kg/cm²"
    assert f"{imc:kg/m²}"=="(2,45 ± 0,03)x10¹ kg/m²"
    assert f"{imc:si}"=="(2,45 ± 0,03)x10¹ kg/m²"