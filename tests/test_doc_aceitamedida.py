import numpy as np

from LabIFSC2 import *

#você não precisa fazer esse passo de usar
# diretamente o aceitamedida, só estou mostrando
#para explicar o que ocorre na biblioteca
seno=aceitamedida(np.sin)

angulo=Medida(30,0.1,'degree')
resultado=seno(angulo) 
print(f"{resultado:E0}") #(0,500 ± 0,002)
assert np.isclose(resultado.nominal(''),0.5,1e-3)