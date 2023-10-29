from .medida import Medida, montecarlo
import numpy as np

def AceitaMedida(func :callable) -> callable:
    '''Possibilita que qualquer função aceite Medidas como argumentos,
    a função é passada por uma simulação monte carlo com as Medidas
    como variáveis gaussianas, é retornada uma Medida como resultado final
    
    Métodos como probabilidade, hist, continuam acessiveis, exemplos:

    import numpy as np

    sin=Aceita(np.sin)

    x=Medida(2,0.1)

    sin(x) # (0.90 +- 0.04)
    
    sin(x,probabilidade=[0.8,0.9]) # 40%

    valor, histograma=sin(x,hist=True)

    plt.hist(histograma,bins=200)

    '''
    
    def FuncaoLabificada(*args,**kargs):
        if isinstance(args[0],Medida):
            result=montecarlo(func,*args,**kargs)
           
            return result
        else:
            return func(*args,**kargs)
    return np.vectorize(FuncaoLabificada)

sin=AceitaMedida(np.sin)
cos=AceitaMedida(np.cos)
tan=AceitaMedida(np.tan)
arcsin=AceitaMedida(np.arcsin)
arccos=AceitaMedida(np.arccos)
arctan=AceitaMedida(np.arctan)
log=AceitaMedida(np.log)
ln=log
log2=AceitaMedida(np.log2)
log10=AceitaMedida(np.log10)
sinh=AceitaMedida(np.sinh)
cosh=AceitaMedida(np.cosh)
tanh=AceitaMedida(np.tanh)
arcsinh=AceitaMedida(np.arcsinh)
arccosh=AceitaMedida(np.arccosh)
arctanh=AceitaMedida(np.arctanh)
exp=AceitaMedida(np.exp)
exp2=AceitaMedida(np.exp2)
sqrt=AceitaMedida(np.sqrt)
cbrt=AceitaMedida(np.cbrt)
power=AceitaMedida(np.power)
    
__all__ = [ 'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 
           'log', 'ln', 'log2', 'log10', 'sinh', 'cosh', 'tanh', 
           'arcsinh', 'arccosh', 'arctanh', 'exp', 'exp2', 'sqrt', 
           'cbrt', 'power','funcoes_matematicas']
funcoes_matematicas=__all__
