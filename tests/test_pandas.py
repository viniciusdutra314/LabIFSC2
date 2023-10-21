import pandas as pd
import numpy as np
from LabIFSC2 import *
theta=np.array([Medida(x,0.01) for x in np.linspace(0,3,10)])
senos=sin(theta)
df=pd.DataFrame(data={'angulos':theta, 'senos':senos})
def test_tabela_angulos():
    global df
    assert np.array_equal(df['angulos'].values,theta)
    assert np.array_equal(df['senos'].values,senos)
def test_tabela_estatistica():
    global df
    assert np.isclose(df['senos'].mean(),0.598478311701527,atol=1e-4)
    assert np.isclose(df['angulos'].mean(),1.5)
    assert np.isclose(df['angulos'].median(),1.5)
    assert np.isclose(df['angulos'].std(),1.0093110847743818,atol=1e-4)
    assert np.isclose(df['angulos'].skew(),0)
