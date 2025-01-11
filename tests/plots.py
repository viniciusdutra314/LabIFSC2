import matplotlib.pyplot as plt
import numpy as np

from LabIFSC2 import Medida, curva_max, curva_min, exp, nominais, sin


def test_plot_gravidade():
    t=np.linspace(1,10,100)
    g=Medida(9.5,0.5)
    y=(g/2)*(t**2)
    plt.plot(t,nominais(y),color='r')
    plt.fill_between(t,curva_min(y),curva_max(y),alpha=0.3)
    
def test_exponencial():   
    t=np.linspace(1,3,100)
    k=Medida(3,0.2)
    y=exp(-k*t)
    plt.plot(t,nominais(y),color='r')
    plt.fill_between(t,curva_min(y),curva_max(y),alpha=0.3)
    
    
def test_seno():
    t=np.linspace(1,3,100)
    w=Medida(3,0.1)
    phi=Medida(0.3,0.02)
    A=Medida(7,0.2)
    y=A*sin(w*t+phi)
    plt.plot(t,nominais(y),color='r')
    plt.fill_between(t,curva_min(y),curva_max(y),alpha=0.3)
    
