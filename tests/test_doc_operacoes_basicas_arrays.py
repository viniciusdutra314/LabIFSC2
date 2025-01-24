from LabIFSC2 import *


def test_doc_operacoes_basicas_arrays():
    import numpy as np

    x=np.array([Medida(1,0.01,'m'),Medida(2,0.01,'m')])
    y=np.array([Medida(200,1,'cm'),Medida(400,1,'cm')])

    print(x+y)#[(3,00 ± 0,01) m (6,00 ± 0,01) m]
    print(x-y)#[(-1,00 ± 0,01) m (-2,00 ± 0,01) m] 
    print(x*y)#[(2,00 ± 0,02) m² (8,00 ± 0,04) m²] 
    print(x/y)#[(5,00 ± 0,06)x10⁻¹  (5,00 ± 0,03)x10⁻¹ ] 
    print(y**2)#[(4,00 ± 0,04)x10⁴ cm² (1,600 ± 0,008)x10⁵ cm²]

    assert np.isclose((x+y)[0].nominal('m'),3,rtol=1e-3)
    assert np.isclose((x-y)[1].nominal('m'),-2,rtol=1e-3)
    assert np.isclose((x*y)[1].nominal('m²'),8,rtol=1e-3)
    assert np.isclose((x/y)[1].nominal(''),5e-1,rtol=1e-3)
    assert np.isclose((y*y)[1].nominal('cm²'),1.6e5,rtol=1e-3)







