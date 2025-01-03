from collections.abc import Callable
from numbers import Number
from typing import Callable
from functools import total_ordering


import numpy as np
from .strong_typing import obrigar_tipos
from .formatacoes import *
from .sistema_de_unidades import TODAS_UNIDADES, Unidade


def montecarlo(func : Callable[[Number,...],Number], 
               *parametros : [Number,...]) -> 'Medida':
    '''## Propagação de erros usando Monte Carlo
  Calcula a média e desvio padrão da densidade de probabilidade de uma 
  função com variáveis gaussianas, também armazena o histograma
  inteiro dentro de uma Medida

  Globals:
    num_montecarlo : Quantidade de números aleatórios usados (Default=10.000)
    pode ser alterado globalmente usando num_montecarlo(valor)

  Args:
    func (callable): função para a propagação do erro
    parametros list[Medida]: parâmetros da função definida acima
  
  Returns:
    Resultado (Medida):  Medida com \(\mu\), \(\sigma\) e histograma
  
  Raises:
        TypeError: Se `func` não for callable ou se algum dos `parametros` não 
        for uma instância de Medida   

'''
    #from . import num_gaussianos

    N=int(1e4)
    if not callable(func): raise TypeError("Func precisa ser um callable (função)")
    x_samples=np.empty((len(parametros),N))
    for index,parametro in enumerate(parametros):
        if not isinstance(parametro,Medida): 
            raise TypeError("Todos os parametros precisam ser Medidas")      
        if not len(parametro.histograma):
            x_samples[index]=np.random.normal(parametro.nominal,
                                              parametro.incerteza,size=N)
        else:
            x_samples[index]=parametro.histograma
    histograma=np.vectorize(func)(*x_samples)
    mean=np.mean(histograma)
    std=np.std(histograma,mean)
    return Medida(mean,std,histograma=histograma)

class Medida:
    def __init__(self,nominal:Number,incerteza : Number=0,
                 unidade : str ="",
                 histograma : np.ndarray = np.array([])):
        """
        Inicializa uma instância da classe Medida com um valor nominal, incerteza e unidade.
        Valor numérico se entende como qualquer objeto que possa interagir normalmente com floats,

        Parâmetros:
            - nominal: Um valor numérico que representa o valor nominal da medida.
            - incerteza: Um valor numérico que representa a incerteza associada à medida.
            - unidade: Uma string que descreve a unidade da medida.

        Raises:
            - TypeError: Se o nominal ou incerteza não puderem ser convertidos para um número.
            - TypeError: A unidade precisa ser uma string
        """
        if incerteza<0:
            raise ValueError("Incerteza não pode ser negativa")
        
        self.nominal=nominal
        self.incerteza=incerteza
        self.histograma=histograma

    def __neg__(self):
        return Medida(-self.nominal,self.incerteza)
    
    def __add__(self,outro):
        #Como existe solução analítica da soma entre duas gaussianas
        #iremos usar esse resultado para otimizar o código
        if isinstance(outro,np.ndarray):
           self_broadcast=np.repeat(self,len(outro))
           return self_broadcast + outro
        outro=self._torna_medida(outro)
        self._checa_dimensao(outro.unidade.simbolo)
        media=self.si_nominal+outro.si_nominal
        desvio_padrao=np.sqrt(self.si_incerteza**2 + outro.si_incerteza**2)
        unidade=self._unidade_mais_proxima(outro.unidade,media)
        media=media*unidade.cte_mult + unidade.cte_ad
        desvio_padrao=desvio_padrao*unidade.cte_mult
        return Medida(media,desvio_padrao,unidade.simbolo)

    def __eq__(self,outro):
        raise TypeError("Como a comparação entre Medidas pode gerar três resultados \
diferentes: iguais, diferentes, ou inconclusivo, optamos por fazer uma função separada \
chamada compara_medidas(x:Medida,y:Medida) -> [Iguais | Diferentes | Inconclusivo], por favor \
não use !=,==,<=,<,>,>= diretamente com Medidas")
    __neq__=__lt__=__le__=__gt__=__ge__=__eq__
    
    def __sub__(self,outro):
        if isinstance(outro,np.ndarray):
           self_broadcast=np.repeat(self,len(outro))
           return self_broadcast - outro
        outro=self._torna_medida(outro)
        media=self.nominal-outro.nominal
        desvio_padrao=np.sqrt(self.incerteza**2 + outro.incerteza**2)
        return Medida(media,desvio_padrao)
    __radd__=__add__
    __rsub__=__sub__
    def __mul__(self,outro):
        if not isinstance(outro,Medida) and not isinstance(outro,np.ndarray):
            constante=outro
            return Medida(self.nominal*constante,(self.incerteza*abs(constante)))
        elif isinstance(outro,np.ndarray):
           self_broadcast=np.repeat(self,len(outro))
           return self_broadcast * outro
        else:
            return montecarlo(lambda x,y: x*y,self,outro)

    def __truediv__(self, outro):
        if not isinstance(outro,Medida) and not isinstance(outro,np.ndarray):
            constante=outro
            return Medida(self.nominal/constante,(self.incerteza/abs(constante)))
        elif isinstance(outro,np.ndarray):
           self_broadcast=np.repeat(self,len(outro))
           return self_broadcast / outro
        else:
            return montecarlo(lambda x,y: x/y,self,outro)
    def __rtruediv__(self, outro):
        outro=self._torna_medida(outro)
        return montecarlo(lambda x,y: y/x,self,outro)
    def __pow__(self,outro):
        if isinstance(outro,np.ndarray):
           self_broadcast=np.repeat(self,len(outro))
           return self_broadcast ** outro
        outro=self._torna_medida(outro)
        return montecarlo(np.power,self,outro)
    def __rpow__(self,outro):
        outro=self._torna_medida(outro)
        return montecarlo(np.power,outro,self)
    def __abs__(self):
        return Medida(abs(self.nominal),self.incerteza)

    
    def probabilidade(self,a:Number,b:Number) -> Number:
        ''' Retorna a probabilidade que a Medida
        esteja entre [a,b] usando o histograma como
        referencia

        Args:
            a (float): Extremo inferior
            b (float): Extremo superior

        Returns:
            probabilidade: (float) probabilidade de estar entre [a,b]
        
        '''

        if not len(self.histograma):
            self.histograma=np.random.normal(self.nominal,
                        self.incerteza,10_000) #hard coded 
        condition=np.logical_and(self.histograma>=a,self.histograma<=b)
        chance=np.count_nonzero(condition)/len(self.histograma)
        return chance


@obrigar_tipos
def equivalente(medida1 : Medida, medida2 : Medida, sigmas : Number )-> bool | None:
    '''Critério de equivalência customizável, escolha
    até quantos sigmas duas Medidas são consideradas iguais
    (Na classe Medida, por padrão são 2 sigmas)

    Exemplo:
        x=Medida(1.0 , 0.05)
        y=Medida(0.7, 0.05)
        
        x.equivalente(y,3) # True

        x - y = 0.3 +- 0.1
        Com dois sigmas elas são consideradas diferentes,
        porém com 3 sigmas elas são equivalentes
    '''
    
    if (sigmas<=0):
        raise ValueError("Sigmas precisa ser um valor maior do que 0")
    delta_nominal=abs(medida1.nominal - medida2.nominal)
    delta_incerteza=abs(medida1.incerteza + medida2.incerteza)
    return delta_nominal<=sigmas*delta_incerteza

