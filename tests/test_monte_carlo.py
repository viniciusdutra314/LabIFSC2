from LabIFSC2 import *
import math ;  from math import isclose
from random import random, randint 
import numpy as np
import pytest

def test_operacoes_basicas():
   for _ in range(100):
      media1=random()+1;sigma1=(random() +1)*0.01
      media2=random()+1; sigma2=(random() +1)*0.01
      a_float= media1
      b_float= media2
      a=Medida(media1,sigma1)
      b=Medida(media2,sigma2)
      assert a+b == a_float+b_float
      assert a*b ==a_float*b_float
      assert a_float**b_float==a**b
      assert a_float/b_float==a/b
      assert a_float-b_float==a-b

def test_iteracao_Medida_float():
   for _ in range(10):
      media1=random()+1;sigma1=(random() +1)*0.01
      media2=random()+1; sigma2=(random() +1)*0.01
      a_float= media1
      b_float= media2
      a=Medida(media1,sigma1)
      b=Medida(media2,sigma2)
      assert a_float+b==a+b_float
      assert a*b_float==a_float*b
      assert a_float**b==a**b_float
      assert a/b_float==a_float/b
      assert a_float-b==a-b_float

def test_iteracao_Medida_int():
   for _ in range(10):
      media1=randint(10,50);sigma1=randint(10,50)*0.1
      media2=randint(30,80);sigma2=randint(30,80)*0.1
      a_float= media1
      b_float= media2
      a=Medida(media1,sigma1)
      b=Medida(media2,sigma2)
      assert a_float+b==a+b_float
      assert a*b_float==a_float*b
      assert a_float**b==a**b_float
      assert a/b_float==a_float/b
      assert a_float-b==a-b_float

def test_probabilidade(): #68-95-99.7 rule

  for _ in range(10):
      media, sigma=random(),random() #gaussianas aleatorias
      a=Medida(media,sigma)
      assert isclose(montecarlo(lambda x:x, a).probabilidade(media-sigma,media+sigma),0.68,abs_tol=0.04)
      assert isclose(montecarlo(lambda x:x, a).probabilidade(media-2*sigma,media+2*sigma),0.95,abs_tol=0.02)
      assert isclose(montecarlo(lambda x:x, a).probabilidade(media-3*sigma,media+3*sigma),0.997,abs_tol=0.01)
      assert montecarlo(lambda x:x, Medida(1,0.1)).probabilidade(media-100000*sigma,media+100000*sigma)==1

def test_exponencias_hiperbolicas():
    for _ in range(100):
      x=Medida(10*np.random.random(),1*np.random.random())
    assert sinh(x)==math.sinh(x.nominal)
    assert cosh(x)==math.cosh(x.nominal)
    assert tanh(x)==math.tanh(x.nominal)
    assert exp(x)==math.exp(x.nominal)
    assert arcsinh(x)==math.asinh(x.nominal) 

def test_acosh(): 
   valores_acosh=[(i,math.acosh(i)) for i in range(2,20)]
   for parametro, valor_esperado in valores_acosh:
    assert arccosh(Medida(parametro,0.2))==Medida(valor_esperado)

def test_atanh():
   valores_atanh=[(i,math.atanh(i)) for i in np.linspace(-0.9,0.9,100)]
   for parametro, valor_esperado in valores_atanh:
    assert arctanh(Medida(parametro,0.02))==Medida(valor_esperado)


def test_wrongvariables():
  a=Medida(7,0.3)
  b=Medida(1,0.1)
  statements=[lambda: montecarlo(lambda x:x,3),
              lambda: montecarlo(lambda x:x,3.13),  
              lambda: montecarlo(lambda x:x,"string"),
              lambda: montecarlo(lambda x:x,a,probabilidade=3),
              lambda: montecarlo(lambda x:x,a,probabilidade=5.1),
              lambda: montecarlo(lambda x:x,a,hist="True"),
              lambda: montecarlo(lambda x:x,a,hist="False"),
              lambda: montecarlo(a)] 
  for index, statement in enumerate(statements):
    with pytest.raises(TypeError):
     statement()
