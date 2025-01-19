from LabIFSC2 import *

imc=Medida(24.5,0.3,'kg/m²')
print(imc.intervalo_de_confiança(0.95))
#[23.91,25.08]

a,b=imc.intervalo_de_confiança(0.95)
assert abs(a-23.91)<0.01 and abs(b-25.08)<0.01 
