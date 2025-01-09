from collections.abc import Callable
from numbers import Number

import numpy as np

from .medida import Medida, montecarlo



def aceitamedida(func :Callable[[Number,...],Number]) -> Callable[[Medida,...],Medida]:
    '''Possibilita que qualquer função aceite e
    retorne Medidas como argumentos
    
    Args:
        func: (callable) Função que não aceita medidas

    Returns:
        func_labificada: (callable) função que aceita e retorna Medidas

    '''
    def FuncaoLabificada(*args):
            args_transformados=[]
            for arg in args:
                if isinstance(arg,Medida):
                    args_transformados.append(arg)
                else:
                    args_transformados.append(Medida(arg,0,''))

            resultado=np.vectorize(montecarlo)(func,*args_transformados)
            if resultado.size==1:
                return resultado.item()
            else:
                return resultado
    return FuncaoLabificada

sin=aceitamedida(np.sin)
seno=sin

cos=aceitamedida(np.cos)

tan=aceitamedida(np.tan)
tg=tan

arcsin=aceitamedida(np.arcsin)
asin=arcsin
arcseno=arcsin

arccos=aceitamedida(np.arccos)
acos=arccos

arctan=aceitamedida(np.arctan)
atan=arctan
arctg=arctan

log=aceitamedida(np.log)
ln=log
log2=aceitamedida(np.log2)
log10=aceitamedida(np.log10)

sinh=aceitamedida(np.sinh)
senh=sinh

cosh=aceitamedida(np.cosh)
tanh=aceitamedida(np.tanh)
tgh=tanh
arcsinh=aceitamedida(np.arcsinh)
asinh=arcsinh
asenh=arcsinh
arccosh=aceitamedida(np.arccosh)
acosh=arccosh
arctanh=aceitamedida(np.arctanh)
atanh=arctanh
atgh=arctanh

exp=aceitamedida(np.exp)
exp2=aceitamedida(np.exp2)
sqrt=aceitamedida(np.sqrt)
cbrt=aceitamedida(np.cbrt)
power=aceitamedida(np.power)
pow=power
    
