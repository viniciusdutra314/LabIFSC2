import matplotlib.pyplot as plt
import numpy as np

from LabIFSC2 import *

campo_magnético=arrayM([210,90,70,54,39,32,33,27,22,20],1,'muT')
distancias=linspace(1,10,10,0.01,'cm') 

unidade_x='cm'
unidade_y='muT'

regressao=regressao_potencia(distancias,campo_magnético)
print(regressao)
plt.style.use('ggplot')
plt.errorbar(nominais(distancias,unidade_x),nominais(campo_magnético,unidade_y),
             xerr=incertezas(distancias,unidade_x),yerr=incertezas(campo_magnético,unidade_y),
             fmt='o',label='Dados experimentais',color='red')

x=linspace(1,10,100,0,unidade_x)
plt.plot(nominais(x,unidade_x),nominais(regressao(x),unidade_y),color='blue',
         label="Curva teórica")
plt.fill_between(nominais(x,unidade_x),curva_min(regressao(x),unidade_y),
                 curva_max(regressao(x),unidade_y),color='blue',alpha=0.3)
plt.legend()
plt.savefig('teste.jpg') 