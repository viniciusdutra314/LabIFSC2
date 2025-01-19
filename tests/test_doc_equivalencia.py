from LabIFSC2 import *

imc1= Medida(25,0.1,'kg/m²')
imc2= Medida(24.5,0.3,'kg/m²')
print(comparar_medidas(imc1,imc2))
#Comparacao.EQUIVALENTES


assert comparar_medidas(imc1,imc2)==Comparacao.EQUIVALENTES