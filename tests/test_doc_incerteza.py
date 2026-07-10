from LabIFSC2 import *


def test_doc_incerteza():
    

    campo_magnético=arrayM([250,150,110,90,70,60,55,40,25,20],'muT',1)
    print(incertezas(campo_magnético,'muT'))
    #[1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]

    assert str(incertezas(campo_magnético,'muT'))=="[1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]"