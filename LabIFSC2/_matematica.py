from collections.abc import Callable
from numbers import Number
from typing import Any

import numpy as np

from ._medida import Medida, montecarlo
from ._tipagem_forte import obrigar_tipos


@obrigar_tipos
def aceitamedida(func :Callable, num_args :int=1) -> Callable:
    def FuncaoLabificada(*args:Any) -> Any:
        args_transformados = [arg if isinstance(arg, Medida) else Medida(arg, 0, '') for arg in args]
        
        if all(not isinstance(arg, Medida) for arg in args): return func(*args)
        else: return montecarlo(func, *args_transformados)    
    funcao_com_numpy= np.frompyfunc(FuncaoLabificada,num_args,1)
    return funcao_com_numpy

'''
Essas são as funções que o LabIFSC2 já implementa para aceitar Medidas,
caso queira adicionar mais funções, basta seguir o padrão abaixo.

Perceba que é possível dar um apelido para a função, por exemplo,
seno=sin, dessa forma, ambos são equivalentes.

Além de aceitar Medidas o decorador aceitamedida também vetoriza a função,
ou seja, se você passar um array de Medidas, ele irá retornar um array de Medidas.
Isso é feito usando a função np.frompyfunc que precisa saber o número de argumentos que
a função recebe, por isso, o argumento num_args é necessário.

Após ter criado a sua função, adicione ela no import _matematetica no __init__.py,
eu não fiz um from ._matematica import * para não sujar o namespace do LabIFSC2. 

'''


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
power=aceitamedida(np.power,2)
pow=power
    


