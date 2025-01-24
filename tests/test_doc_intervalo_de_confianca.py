from LabIFSC2 import *


def test_doc_intervalo_de_confianca():
    imc=Medida(24.5,0.3,'kg/m²')
    print(imc.intervalo_de_confiança(0.95,'kg/m²'))
    #[23.91,25.08]

    a,b=imc.intervalo_de_confiança(0.95,'kg/m²')
    assert abs(a-23.91)<0.01 and abs(b-25.08)<0.01 
