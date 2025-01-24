from LabIFSC2 import *


def test_doc_sqrt_vetorizado():    
    import numpy as np
    areas=np.array([Medida(4,0.01,'cm²'),Medida(9,0.01,'m²'),
                    Medida(16,0.01,'km²')])
    lados=np.sqrt(areas)
    print(lados) #[(2,000 ± 0,003) cm (3,000 ± 0,002) m (4,000 ± 0,001) km]
    #assert str(lados)== "[(2,000 ± 0,003) cm (3,000 ± 0,002) m (4,000 ± 0,001) km]"