from LabIFSC2 import *


def test_doc_sqrt_vetorizado():    
    import numpy as np
    areas=np.array([Medida(4,'cm²',0.001),Medida(9,'m²',0.001),
                    Medida(16,'km²',0.001)])
    lados=np.sqrt(areas)
    assert str(lados) =="[(2,0000 ± 0,0002) cm (3,0000 ± 0,0002) m (4,0000 ± 0,0002) km]"
