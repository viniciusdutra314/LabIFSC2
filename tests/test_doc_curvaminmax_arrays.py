from LabIFSC2 import *


def test_doc_cuvraminmax_arrays():
    curva=linspaceM(0,5,6,'m',0.1)
    print(curva_min(curva,'m'))#[-0.2  0.8  1.8  2.8  3.8  4.8]
    print(curva_max(curva,'m'))##[0.2 1.2 2.2 3.2 4.2 5.2]
    

    print(curva_min(curva,'m',4))#[-0.4  0.6  1.6  2.6  3.6  4.6]
    print(curva_max(curva,'m',4))#[0.4 1.4 2.4 3.4 4.4 5.4]

