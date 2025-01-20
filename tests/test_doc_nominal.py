from LabIFSC2 import *

campo_magnético=arrayM([250,150,110,90,70,60,55,40,25,20],1,'muT')
print(nominais(campo_magnético,'muT'))
#[250. 150. 110.  90.  70.  60.  55.  40.  25.  20.]

assert str(nominais(campo_magnético,'muT'))=="[250. 150. 110.  90.  70.  60.  55.  40.  25.  20.]"