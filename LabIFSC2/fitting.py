import numpy as np
from numpy.polynomial import Polynomial
from .medida import Medida
from .matematica import exp
from .arrayM import Nominais

class MPolinomio(Polynomial):
   '''
   Cria polinômios que aceitam Medidas como coeficientes,
   A ordem dos coeficientes é de grau crescente 
   Exemplo:

   x=[Medida(3,0.3),Medida(5,1),Medida(7,0.01)]
   print(MPolinomio(x))

   (3±0.3) + (5±1)·x + (7±0.01)·x²


   '''
   def derivada(self,n=1):
        '''Calcula a enesima derivada, por padrão n=1
                Retorna um objeto da classe MPolinomio'''
        try: n=int(n)
        except: raise TypeError("A ordem da derivada precisa ser convertida para int")

        if not n>=1: raise ValueError("A ordem da derivada precisa ser igual ou maior que 1")

        if n>len(self.coef)-1:
            return MPolinomio(0)

        #Vamos inverter a ordem dos coeficientes (agora será decrescente no grau)
        #somente para facilitar o código, depois os coeficientes voltaram ao normal

        coef_dec=self.coef[::-1] ; novos_coef=coef_dec

        def loop_derivada(coef_dec):     
            grau=len(coef_dec) -1
            novos_coef=np.zeros(len(coef_dec),dtype=Medida)
            for i in range(grau):
                novos_coef[i] = coef_dec[i] * (grau - i)
            return novos_coef

        for _ in range(n): 
            novos_coef=loop_derivada(novos_coef)
            novos_coef=novos_coef[novos_coef!=0]

        return MPolinomio(novos_coef[::-1])
   def raizes(self):
        '''Retorna uma lista com as raizes do seu polinômio,
        para o cálculo, é considerado que os coeficientes não 
        possuem incertezas
        '''
        from numpy.polynomial import polyutils as pu
        novos_coef=np.zeros(len(self.coef))
        for index,coef in enumerate(self.coef):
          novos_coef[index]=coef
        roots = self._roots(novos_coef)
        return pu.mapdomain(roots, self.window, self.domain)   
   def roots(self):
        return self.raizes()
   def coef_pelas_raizes(raizes : list or np.ndarray):
        '''Fornecendo as raizes do polinômio, é possível calcular
        os seus coeficientes atráves da formula
        
           y=(x-r1)(x-r2)(x-r3)...

        As raizes podem ser Medidas, nesse caso os coeficientes
        possuem incerteza
        '''

        if not isinstance(raizes,np.ndarray):
            raizes=np.array(raizes)
        from itertools import combinations
        coefs=np.zeros(len(raizes)+1,dtype=Medida)
        coefs[0]=1
        def girard(combinacoes : iter) -> float:
            soma=0; 
            for tuplas in combinacoes:
                produto=1
                for elemento in tuplas:
                    produto*=elemento
                soma+=produto
            return soma
        for j in range(1,len(raizes)+1):
            combinacoes=combinations(raizes,j)
            coefs[j]=((girard(combinacoes))*(-1)**(j))
        return MPolinomio(coefs[::-1]) 
   def fromroots(self,raizes):
     return self.coef_pelas_raizes(raizes) 


def regressao_polinomial(x:iter,y:iter,grau : int =1) -> MPolinomio:
    '''Encontre o melhor polinômio em termos de erro
        quadrático para os seus dados
    Args:
        x , y  : iterables (arrays,list,...) com floats ou Medidas

        grau : int , grau do polinômio
    Return : 
        MPolinomio com os coeficientes
    '''
    coeficientes, covarianca=np.polyfit(x,y,grau,cov=True)
    erros=np.sqrt(np.diag(covarianca))
    coeficientes_medidas=np.empty(len(coeficientes),dtype=Medida)
    for j in range(len(coeficientes)):
        coeficientes_medidas[j]=Medida(coeficientes[j],erros[j])
    return MPolinomio(coeficientes_medidas[::-1])

def regressao_linear(x:iter,y:iter) -> MPolinomio:
    '''Encontre a melhor reta (minímos quadrados)
    
    y = a * x + b

    Args:
        x , y iterables (arrays,list,...) com floats ou Medidas
    Return : 
        MPolinomio com os coeficientes
    '''

    return regressao_polinomial(x,y,1)

def regressao_exponencial(x: iter,y:iter) -> np.ndarray(Medida):
    '''Encontre a melhor exponencial da forma
    y = a * exp(-k*x)

    Args:
        x , y iterables (arrays,list,...) com floats ou Medidas
    Return:
        list com Medidas a , k
    '''
    x_nominal=Nominais(x) ; y_nominal=Nominais(x)
    coefs=regressao_linear(x,np.log(y)).coef
    return np.array([exp(coefs[0]),coefs[1]])

def regressao_potencia(x : iter , y: iter) -> np.ndarray(Medida):
    '''Encontra a melhor lei de potência
       
       y=A * (x^n)  
    
    Args:
        x , y iterables (arrays,list,...) com floats ou Medidas
    Return:
        list com Medidas a , n
    '''
    x_nominal=Nominais(x) ; y_nominal=Nominais(x)
    coefs=regressao_linear(np.log(x_nominal),np.log(y_nominal)).coef
    return np.array([np.exp(coefs[0]), coefs[1]])
