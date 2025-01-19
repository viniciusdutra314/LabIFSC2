import numpy as np

from LabIFSC2 import *

x=np.array([Medida(1,0.01,'m'),Medida(2,0.01,'m')])
y=np.array([Medida(200,1,'cm'),Medida(400,1,'cm')])

print(x+y)#[(3,00 ± 0,01) m (6,00 ± 0,01) m]
print(x-y)#[(-1,00 ± 0,01) m (-2,00 ± 0,01) m] 
print(x*y)#[(2,00 ± 0,02) m² (8,00 ± 0,04) m²] 
print(x/y)#[(5,00 ± 0,06)x10⁻¹  (5,00 ± 0,03)x10⁻¹ ] 
print(y**2)#[(4,00 ± 0,04)x10⁴ cm² (1,600 ± 0,008)x10⁵ cm²]










