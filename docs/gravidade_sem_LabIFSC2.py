from LabIFSC2 import *

#g=4π²L/T²
L=Medida(150,1,'cm')
T=Medida(780,1,'ms')
g=(4*constantes.pi**2)*L/T**2
g._converter_para_si()
print(g) #(9,73 ± 0,07)x10¹ m/s²
print(f"{g:latex}") 
'''9,73 \, \pm \, 0,07)\times 10^{1} \, 
\frac{\mathrm{m}}{\mathrm{s}^{2}}'''