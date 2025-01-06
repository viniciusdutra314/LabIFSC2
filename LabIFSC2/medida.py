from collections.abc import Callable
from numbers import Number
from typing import Callable
from functools import total_ordering


import numpy as np
from .strong_typing import obrigar_tipos
from .formatações import *
from enum import Enum


def montecarlo(func : Callable, 
               *parametros : [Number,...],N:int=100_000) -> 'Medida':
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
    x_samples=np.empty((len(parametros),N))
    for index,parametro in enumerate(parametros):
        if not (len(parametro._histograma)):
            x_samples[index]=np.random.normal(parametro.nominal,
                                              parametro.incerteza,size=N)
        else:
            x_samples[index]=parametro._histograma
    histograma=np.vectorize(func)(*x_samples)
    mean=np.mean(histograma)
    std=np.std(histograma,mean=mean)
    resultado=Medida(mean,std,'')
    resultado._histograma=histograma
    resultado._gaussiana=False
    return resultado

class Medida:
    @obrigar_tipos(in_class_function=True)
    def __init__(self,nominal:Number,incerteza : Number,
                 unidade : str ):
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
        if incerteza<0: raise ValueError("Incerteza não pode ser negativa")
        self._nominal=nominal
        self._incerteza=incerteza
        self._unidade=unidade

        self._gaussiana=True
        self._histograma=np.array([])


    def _erro_por_mudar_atributo(self):
        raise PermissionError("Para garantir a integridade da Medida realizada \
o LabIFSC2 não permite a alteração direta de nominal, incerteza, unidade (somente leitura).\
Caso precise de uma nova Medida, crie outra com o \
construtor padrão Medida(nominal, incerteza, unidade)")

    @property
    def nominal(self) -> Number: return self._nominal
    
    @nominal.setter
    def nominal(self, value):self._erro_por_mudar_atributo()
    
    @nominal.deleter
    def nominal(self): self._erro_por_mudar_atributo()

    @property
    def incerteza(self) -> Number: return self._incerteza
    
    @incerteza.setter
    def incerteza(self, value): self._erro_por_mudar_atributo()
    
    @incerteza.deleter
    def incerteza(self): self._erro_por_mudar_atributo()

    @property
    def unidade(self) -> str: 
        return self._unidade
    
    @unidade.setter
    def unidade(self, value): self._erro_por_mudar_atributo()
    
    @unidade.deleter
    def unidade(self): self._erro_por_mudar_atributo()

    def __eq__(self,outro):
        raise TypeError("Como a comparação entre Medidas pode gerar três resultados \
diferentes: iguais, diferentes, ou inconclusivo, optamos por fazer uma função separada \
chamada compara_medidas(x:Medida,y:Medida) -> [Iguais | Diferentes | Inconclusivo], por favor \
não use !=,==,<=,<,>,>= diretamente com Medidas")
    __neq__=__lt__=__le__=__gt__=__ge__=__eq__
        

    def __add__(self,outro) -> 'Medida':
        if self is outro: return 2*self

        elif (self._gaussiana and outro._gaussiana):
            #Como existe solução analítica da soma entre duas gaussianas
            #iremos usar esse resultado para otimizar o código
            media=self.nominal+outro.nominal
            desvio_padrao=np.sqrt(self.incerteza**2 + outro.incerteza**2)
            return Medida(media,desvio_padrao,self.unidade)
        else:
            return montecarlo(lambda x,y: x+y,self,outro)

    
    def __sub__(self,outro)-> 'Medida':
        if self is outro: return Medida(0,0,self.unidade)

        elif (self._gaussiana and outro._gaussiana):
            #Como existe solução analítica da subtração entre duas gaussianas
            #iremos usar esse resultado para otimizar o código
            media=self.nominal-outro.nominal
            desvio_padrao=np.sqrt(self.incerteza**2 + outro.incerteza**2)
            return Medida(media,desvio_padrao,self.unidade)
        else:
            return montecarlo(lambda x,y: x+y,self,outro)
    
    

    def __mul__(self,outro)-> 'Medida':
        if self is outro: return montecarlo(lambda x: x**2,self)
        elif isinstance(outro,Medida):
            return montecarlo(lambda x,y: x*y,self,outro)
        elif isinstance(outro,Number):
            resultado=Medida(self.nominal*outro,abs(self.incerteza*outro),self.unidade)
            resultado._histograma=self._histograma*outro
            return resultado
    
    def __truediv__(self, outro) -> 'Medida':
        if self is outro: return Medida(1,0,self.unidade)
        elif isinstance(outro,Number):
            resultado=Medida(self.nominal/outro,(self.incerteza/abs(outro)),self.unidade)
            resultado._histograma=self._histograma/outro
            return resultado
        elif isinstance(outro,Medida):
            return montecarlo(lambda x,y: x/y,self,outro)

    def __pow__(self,outro) -> 'Medida':
        if isinstance(outro,Number):
           return montecarlo(lambda x: np.pow(x,outro),self)
        elif isinstance(outro,Medida):
            return montecarlo(lambda x,y: x**y,self,outro)


    __radd__=__add__
    __rsub__=__sub__
    __rmul__=__mul__
    __rtruediv__=__truediv__
    __rpow__=__pow__

    def __abs__(self) -> 'Medida':
        return Medida(abs(self.nominal),self.incerteza,self.unidade)
    
    def __neg__(self) -> 'Medida': 
        resultado=Medida(-self.nominal,self.incerteza,self.unidade)
        resultado._histograma=-self._histograma
        return resultado
        
    def __pos__(self) -> 'Medida': 
        resultado=Medida(self.nominal,self.incerteza,self.unidade)
        resultado._histograma=self._histograma
        return resultado
    

    def probabilidade(self,a:Number,b:Number) -> Number:
        ''' Retorna a probabilidade que a Medida
        esteja entre [a,b] usando o histograma como
        referencia

        Args:
            `a` (Number): Extremo inferior
            `b`(Number): Extremo superior

        Returns:
            `probabilidade`: (Number) probabilidade de estar entre [a,b]
        
        Raises:
            ValueError: Se `a` for maior que `b`
        '''

        if a>b: raise ValueError("a deve ser menor que b")

        if not len(self._histograma):
            self._histograma=np.random.normal(self.nominal,
                        self.incerteza,10_000) #hard coded 
            
        return np.mean((self._histograma >= a) & (self._histograma <= b))



class Comparacao(Enum):
    IGUAIS = "iguais"
    DIFERENTES = "diferentes"
    INCONCLUSIVO = "inconclusivo"

@obrigar_tipos()
def comparar_medidas(medida1: Medida, medida2: Medida, 
    sigmas_customizados: list[Number] = [2, 3]) -> Comparacao:
    """
    Compara duas medidas considerando suas incertezas e retorna o resultado da comparação.

    Args:
        `medida1` (Medida) A primeira medida a ser comparada.

        `medida2` (Medida) A segunda medida a ser comparada.

        `sigmas_customizados` (list[Number], opcional): Lista contendo dois valores sigma. 
            O primeiro sigma é usado para determinar se as medidas são iguais. 
            O segundo sigma é usado para determinar se as medidas são diferentes. 
            O valor padrão é [2, 3].
    
    Returns:
        `Comparacao` (Enum):
        - `Comparacao.IGUAIS`: Se as medidas são consideradas iguais.
        - `Comparacao.DIFERENTES`: Se as medidas são consideradas diferentes.
        - `Comparacao.INCONCLUSIVO`: Se a comparação é inconclusiva.
        
    
    Raises:
        ValueError: Se o sigma para serem consideradas iguais for maior que o sigma para serem diferentes.
    """
                     
    diferenca_nominal=abs(medida1.nominal-medida2.nominal)
    soma_incertezas=medida1.incerteza+medida2.incerteza
    sigma_igual=sigmas_customizados[0]
    sigmal_diferente=sigmas_customizados[1]
    if sigma_igual>sigmal_diferente:
        raise ValueError("Sigma para serem consideradas iguais é maior que o sigma \
para serem diferentes")
    
    
    if diferenca_nominal<sigma_igual*soma_incertezas:
        return Comparacao.IGUAIS
    elif diferenca_nominal>sigmal_diferente*sigmal_diferente:
        return Comparacao.DIFERENTES
    else:
        return Comparacao.INCONCLUSIVO
