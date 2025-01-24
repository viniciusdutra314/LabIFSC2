import math
import re
from collections.abc import Callable
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from numbers import Real
from statistics import NormalDist
from string import Template
from typing import Any

import numpy as np
from pint import Quantity, UnitRegistry
from pint.util import UnitsContainer

from . import MCSamples
from ._tipagem_forte import obrigar_tipos


@obrigar_tipos
def alterar_monte_carlo_samples(novo_valor:int) -> None:
    global MCSamples
    if novo_valor<=0:
        raise ValueError("MCSamples deve ser maior que 0")
    MCSamples=novo_valor
    return None

ureg = UnitRegistry()


def montecarlo(func : Callable,*parametros : 'Medida',) -> 'Medida':
    x_samples=np.empty(len(parametros),dtype=Quantity)
    for index,parametro in enumerate(parametros):
        x_samples[index]=parametro.histograma
    histograma=func(*x_samples)
    mean=np.mean(histograma)
    std=np.std(histograma,mean=mean)
    if (isinstance(histograma,Quantity)):
        resultado=Medida(mean.magnitude,str(histograma.units),std.magnitude)
    else:
        resultado=Medida(mean,"",std)
    resultado._histograma=histograma
    return resultado

class Medida:

    @obrigar_tipos
    def __init__(self,nominal:Real | list,unidade : str,incerteza : Real):
        """
        Representa uma medida física com um valor nominal, incerteza e unidade.

        A classe Medida é usada para converter unidades e propagar incertezas
        de maneira simples, se comportando para vários propósitos como um número

        Atributos:
            nominal (Real): O valor nominal da medida.
            incerteza (Real): A incerteza associada à medida.
            unidade (str): A unidade da medida.
        """
        if incerteza<0: raise ValueError("Incerteza não pode ser negativa")

        if isinstance(nominal,list):
            if len(nominal)<2:
                raise ValueError("Lista de medidas deve ter pelo menos 2 elementos")
            mean=np.average(nominal)
            std=np.std(nominal,mean=mean)
            self._nominal= ureg.Quantity(mean,unidade).to_reduced_units()
            if std>incerteza:
                self._incerteza=ureg.Quantity(std,unidade).to_reduced_units()
            else:
                self._incerteza=ureg.Quantity(incerteza,unidade).to_reduced_units()
        else:
            self._nominal=ureg.Quantity(nominal,unidade).to_reduced_units()
            self._incerteza=ureg.Quantity(incerteza,unidade).to_reduced_units()
        self._histograma:Any=None
        self._nominal.ito_reduced_units
        self._incerteza.ito_reduced_units

    @obrigar_tipos
    def nominal(self:'Medida',unidade:str) -> float:
        if unidade.lower()=='si':
            return float(self._nominal.to_base_units().magnitude)
        else:
            return float(self._nominal.to(unidade).magnitude)
    @obrigar_tipos
    def incerteza(self:'Medida',unidade:str) -> float:
        if unidade.lower()=='si':
            return float(self._incerteza.to_base_units().magnitude)
        else:
            return float(self._incerteza.to(unidade).magnitude)

    @property
    def dimensao(self:'Medida') -> UnitsContainer:
        return self._nominal.dimensionality

    @property
    def histograma(self:'Medida') -> Any:
        if self._histograma is None:
            if self._incerteza.magnitude!=0:
                self._histograma=np.random.normal(self._nominal.magnitude,
                                                  self._incerteza.magnitude,
                                                  size=MCSamples)*self._nominal.units
            else:
                self._histograma=self._nominal
        return self._histograma

    @obrigar_tipos
    def __format__(self, format_spec:str) -> str:


        #parsing format_spec
        format_spec=format_spec.lower()
        match_reg=re.search(r'[+-]?e(\d+)',format_spec) #E3=3, -E1=-1, +E2=2
        fmt_exp=int(match_reg.group(1)) if match_reg else False
        unidade=format_spec.split('_')[0]

        if unidade=='':
            unidade=str(self._nominal.units)
            nominal_pint = self._nominal
            incerteza_pint = self._incerteza
        elif unidade=='si':
            nominal_pint=self._nominal.to_base_units()
            incerteza_pint=self._incerteza.to_base_units()
        elif not (re.search(r'[+-]?e(\d+)',unidade) or 'latex' in unidade):
            nominal_pint=self._nominal.to(unidade)
            incerteza_pint=self._incerteza.to(unidade)
        else:
            nominal_pint = self._nominal
            incerteza_pint = self._incerteza
            unidade=str(self._nominal.units)
        nominal=Decimal(nominal_pint.magnitude)
        incerteza=Decimal(incerteza_pint.magnitude)

        exato= (incerteza==0)
        latex= ('latex' in format_spec)
        #templates
        template_console=Template(r"($nominal ± $incerteza)$potencia $unidade")
        template_console_exato=Template(r"$nominal$potencia $unidade")
        template_latex=Template(r"($nominal \, \pm \, $incerteza)$potencia \, $unidade")
        template_latex_exato=Template(r"$nominal$potencia \, $unidade")



        og_nominal = math.floor(math.log10(abs(nominal))) if nominal else 0

        if fmt_exp is False:
            nominal *= Decimal(f"1e{-og_nominal}")
            incerteza *= Decimal(f"1e{-og_nominal}")
        else:
            nominal *= Decimal(f"1e{-fmt_exp}")
            incerteza *= Decimal(f"1e{-fmt_exp}")

        #arredondando nominal e incerteza
        og_incerteza = math.floor(math.log10(abs(incerteza))) if incerteza else 0
        arred_nominal = nominal.quantize(Decimal(f'1e{og_incerteza}'), rounding=ROUND_HALF_UP) if not exato else nominal
        arred_incerteza = incerteza.quantize(Decimal(f'1e{og_incerteza}'), rounding=ROUND_HALF_UP) if not exato else incerteza
        arred_nominal_str = str(arred_nominal).replace(".", ",")
        arred_incerteza_str = str(arred_incerteza).replace(".", ",")

        #potencia bonitinha
        expoente_normalizacao=fmt_exp if fmt_exp is not False else og_nominal
        if expoente_normalizacao==0: potencia_bonita=''
        elif latex:
            potencia_bonita=rf"\times 10^{{{expoente_normalizacao}}}"
        elif not latex:
            superscript_map = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹','-': '⁻'}
            potencia_bonita = 'x10'+''.join(superscript_map[char] for char in str(expoente_normalizacao))

        #escolhendo template
        if exato:
            if latex: template = template_latex_exato
            else: template = template_console_exato
        else:
            if latex: template = template_latex
            else: template = template_console

        unidade=f"{nominal_pint.units:~L}" if latex else f"{nominal_pint.units:~P}"
        return template.substitute(nominal=arred_nominal_str,incerteza=arred_incerteza_str,
                                           potencia=potencia_bonita,unidade=unidade)
    
    def __str__(self) -> str:
        printado:str=self.__format__('')
        return printado
    def __repr__(self) -> str:
        representacao:str=self.__format__('')
        return representacao
    
    '''O método abaixo faz a magia que basicamente qualquer função do numpy possa
    ser aplicada diretamente em uma medida
    '''
    def __getattr__(self, func_name:str) -> Any:
        funcoes_suportadas=['sin','cos','exp','sqrt',"sinh","cosh","tanh","arcsinh","arccosh",
                            "arctanh","cbrt","power","pow",
                            'tan','arcsin','arccos','arctan','log','log2','log10']
        if func_name not in funcoes_suportadas:
            raise AttributeError
        else:
            func=getattr(np,func_name)
            def funcao_recebe_medida() -> Any: return montecarlo(func, self)
            return funcao_recebe_medida
    def _adicao_subtracao(self,outro: 'Medida',positivo:bool) -> 'Medida':
        if not (isinstance(outro,Medida) or isinstance(outro,Real)):
            return NotImplemented
        if isinstance(outro,Real):
            self._nominal+=outro
            self._histograma+=outro
            return self

        if self._nominal.is_compatible_with(outro._nominal):
            if self is outro:
                return 2*self if positivo else Medida(0,str(self._nominal.units),0)

            elif (self._histograma is None and outro._histograma is None):
                #Como existe solução analítica da soma/subtração entre duas gaussianas
                #iremos usar esse resultado para otimizar o código
                if positivo: media=self._nominal+outro._nominal
                else: media=self._nominal-outro._nominal
                desvio_padrao=(self._incerteza**2 + outro._incerteza**2)**(1/2)
                desvio_padrao.ito(media.units)
                return Medida(media.magnitude,str(media.units),desvio_padrao.magnitude)
            else:
                if positivo: return montecarlo(lambda x,y: x+y,self,outro)
                else : return montecarlo(lambda x,y: x-y,self,outro)
        else:
            raise ValueError(f"A soma/subtração entre {self._nominal.dimensionality} e \
{outro._nominal.dimensionality} não é possível")

    def __add__(self:'Medida',outro:Any) -> 'Medida':
        return self._adicao_subtracao(outro,True)
    def __sub__(self:'Medida',outro:Any)-> 'Medida':
        return self._adicao_subtracao(outro,False)

    def __mul__(self:'Medida',outro:Any)-> 'Medida':
        if self is outro: return montecarlo(lambda x: x**2,self)
        elif isinstance(outro,Medida):
            return montecarlo(lambda x,y: x*y,self,outro)
        elif isinstance(outro,Real):
            resultado=Medida(self._nominal.magnitude*outro,str(self._nominal.units),abs(self._incerteza.magnitude*outro),)
            if self._histograma is not None:
                resultado._histograma=self._histograma*outro
            return resultado
        else:
            return NotImplemented

    def __truediv__(self:'Medida', outro:Any) -> 'Medida':
        if self is outro: return Medida(1,str(self._nominal.units),0)
        elif isinstance(outro,Real):
            resultado=Medida(self._nominal.magnitude/float(outro),
                             str(self._nominal.units),
                             self._incerteza.magnitude/abs(float(outro)),
                             )
            if self._histograma is not None:
                resultado._histograma=self._histograma/float(outro)
            return resultado
        elif isinstance(outro,Medida):
            return montecarlo(lambda x,y: x/y,self,outro)
        else:
            return NotImplemented

    def __rtruediv__(self:'Medida',outro:Any) -> 'Medida':
        if isinstance(outro,Real):
            return montecarlo(lambda x: outro/x,self)
        else:
            return NotImplemented

    def __pow__(self:'Medida',outro:Any) -> 'Medida':
        if isinstance(outro,Real):
            return montecarlo(lambda x: np.pow(x,float(outro)),self)
        elif isinstance(outro,Medida):
            return montecarlo(lambda x,y: x**y,self,outro)
        else:
            return NotImplemented
    def __rpow__(self:'Medida',outro:Any) -> 'Medida':
        if isinstance(outro,Real):
            return montecarlo(lambda x: np.pow(float(outro),x),self)
        elif isinstance(outro,Medida):
            return montecarlo(lambda x,y: x**y,self,outro)
        else:
            return NotImplemented
    def __eq__(self:'Medida',outro:Any)->bool:
        if self is outro:
            return True
        else:
            raise TypeError("Como a comparação entre Medidas pode gerar três resultados \
    diferentes: iguais, diferentes, ou inconclusivo, optamos por fazer uma função separada \
    chamada compara_medidas(x:Medida,y:Medida) -> [Iguais | Diferentes | Inconclusivo], por favor \
    não use !=,==,<=,<,>,>= diretamente com Medidas")
    def __ne__(self:'Medida',outro:Any)->bool:
        if self is outro:
            return False
        else:
            raise TypeError("Como a comparação entre Medidas pode gerar três resultados \
    diferentes: iguais, diferentes, ou inconclusivo, optamos por fazer uma função separada \
    chamada compara_medidas(x:Medida,y:Medida) -> [Iguais | Diferentes | Inconclusivo], por favor \
    não use !=,==,<=,<,>,>= diretamente com Medidas")


    __radd__=__add__
    __rsub__=__sub__
    __rmul__=__mul__

    def __abs__(self:'Medida') -> 'Medida':
        resultado=Medida(abs(self._nominal.magnitude),
                         str(self._nominal.units),
                         self._incerteza.magnitude,)
        if self._histograma is not None:
            resultado._histograma=abs(self._histograma)
        return resultado

    def __neg__(self:'Medida') -> 'Medida':
        resultado=Medida(-(self._nominal.magnitude),
                         str(self._nominal.units),
                         self._incerteza.magnitude,)
        if self._histograma is not None:
            resultado._histograma=-self._histograma
        return resultado

    def __pos__(self) -> 'Medida':
        return self

    @obrigar_tipos
    def probabilidade_de_estar_entre(self,a:Real,b:Real,unidade:str) -> float:
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
        if not self._nominal.is_compatible_with(unidade):
                raise ValueError(f"Unidade {unidade} não é compatível com a unidade da medida")

        if self._histograma is None:
            #estamos resolvendo de maneira análitica
            mu=self._nominal.to(unidade).magnitude
            sigma=self._incerteza.to(unidade).magnitude
            gaussiana=NormalDist(mu,sigma)
            return gaussiana.cdf(float(b))-gaussiana.cdf(float(a))
        else:
            a_quantidade=ureg.Quantity(a,unidade)
            b_quantidade=ureg.Quantity(b,unidade)
            probabilidade= np.mean((self._histograma >= a_quantidade) & (self._histograma <= b_quantidade),dtype=float)
            return float(probabilidade)

    @obrigar_tipos
    def intervalo_de_confiança(self:'Medida',p:Real,unidade:str) -> list:
        ''' Retorna o intervalo de confiança para a Medida
        com base no histograma

        Args:
            `p` (float): Probabilidade de estar dentro do intervalo

        Returns:- p) < 1e-2
            `intervalo`: (tuple) intervalo de confiança

        Raises:
            ValueError: Se `p` não estiver entre 0 e 1
        '''
        if not 0<float(p)<=1: raise ValueError("p deve estar 0 e 1")

        elif p==1: return [float(min(self.histograma.magnitude)),float(max(self.histograma.magnitude))]

        elif self._histograma is None:
            #estamos resolvendo de maneira analítica
            mu=self._nominal.magnitude
            sigma=self._incerteza.magnitude
            gaussiana=NormalDist(mu,sigma)
            limite_inferior=gaussiana.inv_cdf((1-float(p))/2)
            limite_superior=gaussiana.inv_cdf((1+float(p))/2)
            return [limite_inferior,limite_superior]
        else:
            self._histograma.sort()
            self._histograma.ito(unidade)
            num_elements = len(self._histograma)
            selected_elements = int(np.floor(float(p) * num_elements))
            magnitudes = np.array([item.magnitude for item in self._histograma])
            intervals = magnitudes[selected_elements:] - magnitudes[:-selected_elements]

            shortest_interval_index = np.argmin(intervals)
            shortest_interval = [float(self._histograma[shortest_interval_index].magnitude),
                                float(self._histograma[shortest_interval_index + selected_elements].magnitude)]
            return shortest_interval







class Comparacao(Enum):
    EQUIVALENTES = "iguais"
    DIFERENTES = "diferentes"
    INCONCLUSIVO = "inconclusivo"

@obrigar_tipos
def comparar_medidas(medida1: Medida, medida2: Medida,
    sigma_inferior : float=2,sigma_superior:float=3) -> Comparacao:
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

    diferenca_nominal=abs(medida1._nominal-medida2._nominal)
    soma_incertezas=medida1._incerteza+medida2._incerteza
    if sigma_inferior>sigma_superior:
        raise ValueError("Sigma para serem consideradas iguais é maior que o sigma \
para serem diferentes")

    if diferenca_nominal<sigma_inferior*soma_incertezas:
        return Comparacao.EQUIVALENTES
    elif diferenca_nominal>sigma_superior*soma_incertezas:
        return Comparacao.DIFERENTES
    else:
        return Comparacao.INCONCLUSIVO
