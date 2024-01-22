from .medida import Medida, montecarlo
import numpy as np

def aceitamedida(func :callable) -> callable:
    '''Possibilita que qualquer função aceite Medidas como argumentos,
    a função é passada por uma simulação monte carlo com as Medidas
    como variáveis gaussianas, é retornada uma Medida como resultado final
    
    Args:
        func: (callable) Função que não aceita medidas

    Returns:
        func_labificada: (callable) função que aceita e retorna Medidas

    '''
    
    def FuncaoLabificada(*args,**kargs):
        if isinstance(args[0],Medida):
            result=montecarlo(func,*args,**kargs)
            return result
        else:
            return func(*args,**kargs)
    return np.vectorize(FuncaoLabificada)

sin=aceitamedida(np.sin)
cos=aceitamedida(np.cos)
tan=aceitamedida(np.tan)
arcsin=aceitamedida(np.arcsin)
arccos=aceitamedida(np.arccos)
arctan=aceitamedida(np.arctan)
log=aceitamedida(np.log)
ln=log
log2=aceitamedida(np.log2)
log10=aceitamedida(np.log10)
sinh=aceitamedida(np.sinh)
cosh=aceitamedida(np.cosh)
tanh=aceitamedida(np.tanh)
arcsinh=aceitamedida(np.arcsinh)
arccosh=aceitamedida(np.arccosh)
arctanh=aceitamedida(np.arctanh)
exp=aceitamedida(np.exp)
exp2=aceitamedida(np.exp2)
sqrt=aceitamedida(np.sqrt)
cbrt=aceitamedida(np.cbrt)
power=aceitamedida(np.power)
    
__all__ = ['aceitamedida', 'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 
           'log', 'ln', 'log2', 'log10', 'sinh', 'cosh', 'tanh', 
           'arcsinh', 'arccosh', 'arctanh', 'exp', 'exp2', 'sqrt', 
           'cbrt', 'power','funcoes_matematicas']
funcoes_matematicas=__all__
