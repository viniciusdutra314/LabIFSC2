import numpy as np
from numpy.polynomial import Polynomial

from .strong_typing import obrigar_tipos
from .operacoes_em_arrays import get_nominais
from .matematica import aceitamedida, exp
from .medida import Medida

from collections.abc import Sequence
from numbers import Number
import string

class MPolinomio():
    @obrigar_tipos(in_class_function=True)
    def __init__(self,coeficientes:Sequence[Number | Medida]):
        self._coeficientes=[]
        for index,coef in enumerate(coeficientes):
            if not (isinstance(coef,Number) or isinstance(coef,Medida)):
                raise ValueError('Todos os coeficientes precisam ser números')
            self._coeficientes.append(coef)
            setattr(self,string.ascii_lowercase[index],coef)
        self._grau=len(coeficientes)-1
        self._callable=lambda x:sum(coef*x**(self._grau-i) for i,coef in enumerate(self._coeficientes))
    
    @obrigar_tipos(in_class_function=True)
    def __call__(self,x:Number):
        resultado=0
        for i,coef in enumerate(self._coeficientes):
            resultado+=coef*x**(self._grau-i)
        return resultado
    def __iter__(self):
        return iter(self._coeficientes)

    def __str__(self):
        superscript_map = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
        }
        grau_deixar_bonito=lambda degree: ''.join(superscript_map[digit] for digit in str(degree))
        termos = []
        for i, coef in enumerate(self._coeficientes):
            if coef:
                grau = self._grau - i
                if coef ==1 and grau!=0: 
                    coef=''
                
                if grau == 0:
                    termos.append(f"{coef}")
                elif grau == 1:
                    termos.append(f"{coef}x")
                else:
                    termos.append(f"{coef}x{grau_deixar_bonito(grau)}")
        return " + ".join(termos)

@obrigar_tipos()
def regressao_polinomial(x:np.ndarray,y:np.ndarray,
                         grau:int) -> MPolinomio:
    '''Encontre o melhor polinômio em termos de erro
        quadrático para os seus dados
    Args:
        x , y  : iterables (arrays,list,...) com floats ou Medidas

        grau : int , grau do polinômio
    Return : 
        Array com coeficientes
        func=True:
            MPolinomio(callable)
    '''
    if isinstance(x[0],Medida): x=get_nominais(x) 
    if isinstance(y[0],Medida): y=get_nominais(y)

    coeficientes,lstsq=np.polynomial.Polynomial.fit(x,y,grau,full=True)
    breakpoint()
    covarianca=2
    erros=np.sqrt(np.diag(covarianca))
    coeficientes_medidas=np.empty(len(coeficientes),dtype=Medida)
    for j in range(len(coeficientes)):
        coeficientes_medidas[j]=Medida(coeficientes[j],erros[j])
    return MPolinomio(coeficientes_medidas)

def regressao_linear(x:iter,y:iter,func=False) -> MPolinomio:
    '''Encontre a melhor reta (minímos quadrados)
    
    y = a * x + b

    Args:
        x , y iterables (arrays,list,...) com floats ou Medidas
    Return : 
        Array com Coeficientes
    '''
    return regressao_polinomial(x,y,1,func)

def regressao_exponencial(x,y,base=np.exp(1),func=False):
    '''Encontre a melhor exponencial da forma
    \(y = a * e^{kx}\) para os dados x,y

    É possível mudar a base, por exemplo, 
    base=2 ira encontrar a melhor função

    \(y=a*2^{kx}\)

    Args:
        x (iterable): Medidas ou floats
        y (iterable): Medidas ou floats
        base (float): Base da exponencial
        func (bool): retorna uma função ao invés do fitting
    
    Returns:
        Array (nd.array):  Medidas a , k se func=False
        Função (callable): retorna y(x) se func=True
        
    '''
    x=get_nominais(x) ; y=get_nominais(y)
    assert np.all(y>0), 'Todos y precisam ser positivos para uma modelagem exponencial'
    assert base>1, 'Bases precisam ser maiores que 1'
    coefs=regressao_linear(x,np.log(y)/np.log(base))
    coefs[0]=exp(coefs[0])
    if not func: return coefs
    else:  return aceitamedida(lambda x:coefs[0]*np.power(coefs[1]*x,base))

def regressao_potencia(x, y,func=False) :
    '''Com um conjunto de dados x,y,
    esse método encontra a melhor lei de 
    potência da forma  \(y=A * (x^n)\)

    Args:
        x (iterable): Medidas ou números
        y (iterable): Medidas ou números
        func (bool): Retorna uma função ao invés do fitting
        
    Returns:
        Array (nd.array):  Medidas a , k se func=False
        Função (callable): retorna y(x) se func=True
    '''
    x=get_nominais(x) ; y=get_nominais(y)
    coefs=regressao_linear(np.log(x),np.log(y))
    coefs[0]=exp(coefs[0])
    if not func: return coefs
    else: return aceitamedida(lambda x:coefs[0]*x**coefs[1])
