from LabIFSC2 import *


def test_doc_nominal():
    

    campo_magnético=arrayM([250,150,110,90,70,60,55,40,25,20],'muT',1)
    print(nominais(campo_magnético,'muT'))
    #[250. 150. 110.  90.  70.  60.  55.  40.  25.  20.]

    assert str(nominais(campo_magnético,'muT'))=="[250. 150. 110.  90.  70.  60.  55.  40.  25.  20.]"