from LabIFSC2 import *

x=Medida(1,0.01,'m')
y=Medida(200,1,'cm')
#Operações básicas
print(x+y)#(3,00 ± 0,01) m
print(x-y)#(-1,00 ± 0,01) m 
print(x*y)#(2,00 ± 0,02) m² 
print(x/y)#(5,00 ± 0,06)x10⁻¹ 
print(y**2)#(4,00 ± 0,04)x10⁴ cm²

assert str(x+y)=="(3,00 ± 0,01) m"
assert str(x-y)=="(-1,00 ± 0,01) m"
assert str(x*y)=="(2,00 ± 0,02) m²"
assert str(x/y)=="(5,00 ± 0,06)x10⁻¹ " 
assert str(y**2)=="(4,00 ± 0,04)x10⁴ cm²"


