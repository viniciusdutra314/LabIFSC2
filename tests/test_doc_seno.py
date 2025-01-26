from LabIFSC2 import *


def test_doc_seno_vetorizado():    
    import numpy as np
    theta=Medida(30,'degree',0.01)
    print(np.sin(theta)) #(5,000 ± 0,002)x10⁻¹

    assert str(np.sin(theta))== "(5,000 ± 0,002)x10⁻¹ "
    