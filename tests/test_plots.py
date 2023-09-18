from LabIFSC2 import Medida,Nominais,CurvaMax,CurvaMin
from LabIFSC2 import exp,sin
import numpy as np  
import matplotlib.pyplot as plt
def test_plot_gravidade():
    t=np.linspace(1,10,100)
    g=Medida(9.5,0.5)
    y=(g/2)*(t**2)
    plt.plot(t,Nominais(y),color='r')
    plt.fill_between(t,CurvaMin(y),CurvaMax(y),alpha=0.3)
    plt.show()
    
def test_exponencial():   
    t=np.linspace(1,3,100)
    k=Medida(3,0.2)
    y=exp(-k*t)
    plt.plot(t,Nominais(y),color='r')
    plt.fill_between(t,CurvaMin(y),CurvaMax(y),alpha=0.3)
    plt.show()
    
def test_seno():
    t=np.linspace(1,3,100)
    w=Medida(3,0.1)
    phi=Medida(0.3,0.02)
    A=Medida(7,0.2)
    y=A*sin(w*t+phi)
    plt.plot(t,Nominais(y),color='r')
    plt.fill_between(t,CurvaMin(y),CurvaMax(y),alpha=0.3)
    plt.show()
