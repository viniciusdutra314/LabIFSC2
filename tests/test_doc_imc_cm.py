from LabIFSC2 import *

massa= Medida(75,0.1,'kg')
altura= Medida(175,1,'cm')
imc=massa/altura**2
print(imc) #(2,45 ± 0,03)x10⁻³ kg/cm²
print(f"{imc:kg/m²_E0_LAT}")
print(f"{imc:g/cm²}")
print(f"{imc:si}")

