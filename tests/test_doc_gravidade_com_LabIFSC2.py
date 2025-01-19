from LabIFSC2 import *

#g=4π²L/T²
pi=constantes.pi
L=Medida(15,0.1,'cm')
T=Medida(780,1,'ms')
gravidade=(4*pi**2)*L/T**2
print(f"{gravidade:si}") #(9,73 ± 0,07) m/s²
print(f"{gravidade:si_latex}") 
'''(9,73 \, \pm \, 0,07) \, 
\frac{\mathrm{m}}{\mathrm{s}^{2}}'''

assert f"{gravidade:si}" == "(9,73 ± 0,07) m/s²"
assert f"{gravidade:si_latex}" ==r"(9,73 \, \pm \, 0,07) \, \frac{\mathrm{m}}{\mathrm{s}^{2}}"