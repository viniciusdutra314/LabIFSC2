from LabIFSC2 import *

massa= Medida(75,0.1,'kg')
altura= Medida(1.75,0.01,'m')
imc=massa/altura**2
print(imc) #(2,45 ± 0,03)x10¹ kg/m²
print(imc.intervalo_de_confiança(0.95))
#[23.95, 25.05]
print(imc.nominal+2*imc.incerteza)
print(imc.nominal-2*imc.incerteza)