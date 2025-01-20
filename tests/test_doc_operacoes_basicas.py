from LabIFSC2 import *

x=Medida(1,0.01,'m')
y=Medida(200,1,'cm')
#Operações básicas
print(x+y)#(3,00 ± 0,01) m
print(x-y)#(-1,00 ± 0,01) m 
print(x*y)#(2,00 ± 0,02) m² 
print(x/y)#(5,00 ± 0,06)x10⁻¹ 
print(y**2)#(4,00 ± 0,04)x10⁴ cm²

from numpy import isclose

assert isclose((x+y).nominal('m'),3,1e-2)
assert isclose((x-y).nominal('m'),-1,1e-2)
assert isclose((x*y).nominal('m²'),2,1e-2)
assert isclose((x/y).nominal(''),0.5,1e-2)
assert isclose((y**2).nominal('cm²'),4e4,1e-2)


