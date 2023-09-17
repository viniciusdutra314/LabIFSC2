import numpy as np
from numpy.polynomial import Polynomial

from .medida import Medida

class MPolinomio(Polynomial):
   '''
   
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
        from numpy.polynomial import polyutils as pu
        novos_coef=np.zeros(len(self.coef))
        for index,coef in enumerate(self.coef):
          novos_coef[index]=coef
        roots = self._roots(novos_coef)
        return pu.mapdomain(roots, self.window, self.domain)   
   def roots(self):
        return self.raizes()
   def coef_pelas_raizes(raizes):
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


def regressao_polinomial(x:list,y:list,grau : int =1):
    coeficientes, covarianca=np.polyfit(x,y,grau,cov=True)
    erros=np.sqrt(np.diag(covarianca))
    coeficientes_medidas=np.empty(len(coeficientes),dtype=Medida)
    for j in range(len(coeficientes)):
        coeficientes_medidas[j]=Medida(coeficientes[j],erros[j])
    return coeficientes_medidas[::-1]

def regressao_linear(x:list,y:list,grau:int):
    return regressao_linear(x,y,grau)
