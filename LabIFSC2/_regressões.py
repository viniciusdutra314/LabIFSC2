import string
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from numbers import Real
from typing import Any

import numpy as np
import pint
from numpy import exp, log, power
from numpy.polynomial import Polynomial

from ._medida import Medida, ureg
from ._tipagem_forte import obrigar_tipos


@obrigar_tipos
def _aplicar_funcao_sem_passar_pelo_sistema_de_unidades(
        array_medidas:np.ndarray,lab_func:Callable)->np.ndarray:
    '''
    precisamos aplicar log/exp sem passar pelo sistema de unidades
    um método meio quicky and dirty mas necessário para não dar erro de dimensão
    '''
    medidas_novas=[]
    for medida in array_medidas:
        unidade=str(medida._nominal.units)
        medida_intermediaria=Medida(medida._nominal.magnitude,"",medida._incerteza._magnitude)
        medida_intermediaria=lab_func(medida_intermediaria)
        nominal=medida_intermediaria._nominal._magnitude
        incerteza=medida_intermediaria._incerteza._magnitude
        if np.isnan(nominal) or np.isnan(incerteza):
            raise ValueError(f'Erro ao aplicar {lab_func} no processo de regressão. Lembre-se que, para regressões \
exponenciais, todos os valores de y precisam ser positivos. No caso da regressão de lei de potência, os valores \
em x também precisam ser positivos. Além disso, um valor pode não ser negativo, mas devido à incerteza associada, ele pode assumir valores negativos.')
        medidas_novas.append(Medida(nominal,unidade,incerteza))
    return np.array(medidas_novas)
@obrigar_tipos
def _forcar_troca_de_unidade(array_medidas:np.ndarray,unidade:str)-> np.ndarray:
    return np.array([Medida(med._nominal.magnitude,unidade,med._incerteza.magnitude,) for med in array_medidas])

class Regressao(ABC):
    
    def __init__(self)->None:
        self._amostragem_pre_calculada: np.ndarray = np.array([])
        self._valores: Iterator = iter([])
    
    def _retornar(self,y:np.ndarray,unidade_y:str)->np.ndarray:
        for y_medida in y:
            y_medida._histograma=None
        self._amostragem_pre_calculada=y
        
        resultado:np.ndarray=np.array([x.nominal(unidade_y) for x in self._amostragem_pre_calculada],dtype=float)
        return resultado
    
    def _verificar_tipo_de_x(self,x:np.ndarray)->None:
        if not isinstance(x[0],Medida):
                raise TypeError("x precisa ser um array de medidas ou uma medida \
mesmo que com incerteza 0, pois precisamos das unidades")
        return None
    
    @abstractmethod
    def __repr__(self)->str:...

    @abstractmethod
    def amostrar(self, x:np.ndarray,unidade_y:str) -> np.ndarray:...

    def __iter__(self)->Iterator[object]:
        return self._valores

    def mudar_intervalo_de_confianca(self,sigmas:Real)->None:
        """
        Altera o intervalo de confiança para o valor especificado.
        
        Args:
            sigmas (Real): O novo valor do intervalo de confiança.
        
        Returns:
            None
        """
        if sigmas<0:
            raise ValueError('O intervalo de confiança precisa ser um valor positivo')

        self._sigmas=float(sigmas)



class MPolinomio(Regressao):
    @obrigar_tipos
    def __init__(self,coeficientes:np.ndarray):
        if not (isinstance(coeficientes[0],Medida)):
            raise TypeError('Os valores do array não são Medidas')
    
        self._coeficientes:list[Medida]=[]
        for index,coef in enumerate(coeficientes):
            self._coeficientes.append(coef)
            setattr(self,string.ascii_lowercase[index],coef)
        self.grau=len(coeficientes)-1
    
    @obrigar_tipos
    def amostrar(self:'MPolinomio', x:np.ndarray,unidade_y:str) -> np.ndarray:
        """
        Calcula os valores de um polinômio para um conjunto de entradas x.
        Args:
            x (np.ndarray): Um array de valores nos quais o polinômio será avaliado.
            unidade_y (str): A unidade de medida para os valores calculados do polinômio.
        Returns:
            np.ndarray: Um array contendo os valores calculados do polinômio nas unidades especificadas.
        Raises:
            TypeError: Se o tipo de `x` não for np.ndarray.
        """


        self._verificar_tipo_de_x(x)
        y:Any=Medida(0,unidade_y,0)
        for index,coef in enumerate(self._coeficientes):y+=power(x,self.grau-index)*coef
        polinomio_calculado:np.ndarray=y
        return self._retornar(polinomio_calculado,unidade_y)

    def __iter__(self) -> Iterator[Medida]:
        return iter(self._coeficientes)
    
    def __repr__(self) -> str:
        return f"MPolinomio(coefs={self._coeficientes},grau={self.grau})"



class MExponencial(Regressao):
    '''Classe para modelar uma função exponencial
    y = a * base^(kx)
    '''
    __slots__ = ['cte_multiplicativa', 'expoente', 'base','_valores']
    @obrigar_tipos
    def __init__(self,a:Medida,k:Medida,base:Real):
        self.cte_multiplicativa=a
        self.base=base
        self.expoente=k
        self._valores=iter((a,k,base))
    
    @obrigar_tipos
    def amostrar(self:'MExponencial', x:np.ndarray,unidade_y:str)->np.ndarray:
        """
        Gera uma amostra de valores exponenciais com base nos parâmetros fornecidos.
        Args:
            x (np.ndarray): Um array de valores de entrada.
            unidade_y (str): A unidade dos valores de saída.
        Returns:
            np.ndarray: Um array de valores calculados com base na função exponencial.
        Raises:
            TypeError: Se o tipo de `x` não for np.ndarray.
        """

        self._verificar_tipo_de_x(x)
        y:np.ndarray=np.power(float(self.base),(self.expoente*x))*self.cte_multiplicativa
        return self._retornar(y,unidade_y)
    
    def __repr__(self)->str:
        return f'MExponencial(cte_multiplicativa={self.cte_multiplicativa},expoente={self.expoente},base={self.base})'

class MLeiDePotencia(Regressao):    
    @obrigar_tipos
    def __init__(self, a: Medida, n: Medida,y_unidade:pint.Quantity):
        super().__init__()
        self.cte_multiplicativa = a
        self.potencia = n
        self._valores=iter([a,n])
        self._y_unidade=y_unidade
    
    @obrigar_tipos
    def amostrar(self:'MLeiDePotencia', x:np.ndarray,unidade_y:str) -> np.ndarray:
        """
        Amostra valores baseados na lei de potência.
        Args:
            x (np.ndarray): Array de valores de entrada.
            unidade_y (str): Unidade da variável dependente y.
        Returns:
            np.ndarray: Array de valores amostrados com a unidade especificada.
        Raises:
            ValueError: Se a unidade de x não for compatível com a unidade esperada.
        """

        self._verificar_tipo_de_x(x)
        unidade_expoente=str((x[0]._nominal**self.potencia._nominal).units)
        x=_forcar_troca_de_unidade(x,'')    
        expoente=x**self.potencia
        expoente_medida=_forcar_troca_de_unidade(expoente,unidade_expoente)
        y=expoente_medida*self.cte_multiplicativa
        if not y[0]._nominal.is_compatible_with(self._y_unidade):
            raise ValueError(f'Unidade de x não está correta')
        return self._retornar(y,unidade_y)
    
    def __repr__(self)->str:
        return f'MLeiDePotencia(cte_multiplicativa={self.cte_multiplicativa}, potencia={self.potencia})'



@obrigar_tipos
def regressao_polinomial(x_medidas:np.ndarray,y_medidas:np.ndarray,grau:int) -> MPolinomio:
    """
    Realiza uma regressão polinomial nos dados fornecidos.
    
    Args:
        x_medidas (np.ndarray): Array de medidas para a variável independente.
        y_medidas (np.ndarray): Array de medidas para a variável dependente.
        grau (int): Grau do polinômio a ser ajustado.
    
    Returns:
        MPolinomio: Um objeto representando o polinômio ajustado com coeficientes como medidas.
    
    Raises:
        ValueError: Se `x_medidas` e `y_medidas` não tiverem o mesmo tamanho ou se não houver dados 
        suficientes para o grau do polinômio.
        TypeError: Se `x_medidas` e `y_medidas` não forem arrays de medidas.
    """
    
    if len(x_medidas)!=len(y_medidas):
        raise ValueError("x_dados e y_dados não tem o mesmo tamanho")
    if len(x_medidas)<=grau+1:
        raise ValueError("Não há dados suficientes para um polinômio de grau {grau} (overfitting)")
    if not (isinstance(x_medidas[0],Medida) and isinstance(y_medidas[0],Medida)):
        raise TypeError('x_medidas e y_medidas precisam ser np.ndarray de medidas')
    x_float=np.array([x._nominal.magnitude for x in x_medidas],dtype=float)
    y_float=np.array([y._nominal.magnitude for y in y_medidas],dtype=float)
    p, cov = np.polyfit(x_float, y_float, grau, cov=True)
    erros=np.sqrt(np.diag(cov))
    medidas_coeficientes=[]
    for index in range(len(p)):
        unidade= str((y_medidas[0]._nominal/x_medidas[0]._nominal**(grau-index)).units)
        medidas_coeficientes.append(Medida(p[index],unidade,erros[index]))
    return MPolinomio(np.array(medidas_coeficientes))

@obrigar_tipos
def regressao_linear(x_medidas:np.ndarray,
                     y_medidas:np.ndarray) -> MPolinomio:
    """
    Calcula a regressão linear para um conjunto de medidas.
    
    Args:
        x_medidas (np.ndarray): Array contendo as medidas da variável independente.
        y_medidas (np.ndarray): Array contendo as medidas da variável dependente.
    
    Raises:
        ValueError: Se `x_medidas` e `y_medidas` não tiverem o mesmo tamanho 
    
    Returns:
        MPolinomio: Objeto representando a reta de regressão linear ajustada aos dados.
    """    
    reta:MPolinomio=regressao_polinomial(x_medidas,y_medidas,1)
    return reta

@obrigar_tipos
def regressao_exponencial(x_medidas:np.ndarray,y_medidas:np.ndarray,
                          base:Real=np.exp(1)) -> MExponencial:
    """
    y=ae^{kx}
    Realiza uma regressão exponencial nos dados fornecidos.
    
    Args:
        x_medidas (np.ndarray): Array de medidas da variável independente.
        y_medidas (np.ndarray): Array de medidas da variável dependente.
        base (Real, opcional): Base da exponencial usada, o padrão é o número de Euler (e).
    
    Raises:
        ValueError: Se a base for menor que 1.
        ValueError: Se y_medidas contiver valores negativos ou zero.
        ValueError: Se `x_medidas` e `y_medidas` não tiverem o mesmo tamanho 
    
    Returns:
        MExponencial: Objeto contendo os parâmetros `a` e `k` da regressão exponencial e a base utilizada.
    """
    if any(y._nominal.magnitude <= 0 for y in y_medidas):
        raise ValueError('Todos os valores de y_medidas devem ser positivos e não nulos para a regressão exponencial.')
    if base<1: raise ValueError('Base precisa ser maior que 1')
    pegar_log=lambda x: log(x)/log(float(base))
    log_y_medidas=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(y_medidas,pegar_log) 
    polinomio=regressao_linear(x_medidas,log_y_medidas)
    k=polinomio.a
    a=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(np.array([polinomio.b]),exp)[0]
    k=_forcar_troca_de_unidade(np.array([k]),str((1/x_medidas[0]._nominal).units))
    a=_forcar_troca_de_unidade(np.array([a]),str(y_medidas[0]._nominal.units))
    return MExponencial(a[0],k[0],base)

@obrigar_tipos
def regressao_potencia(x_medidas:np.ndarray, y_medidas:np.ndarray) -> MLeiDePotencia:
    """
    y=a*x^n

    Realiza uma regressão de potência nos dados fornecidos.
    Esta função aplica uma transformação logarítmica aos dados de entrada, realiza uma regressão linear nos dados transformados,
    e então converte os coeficientes da regressão linear de volta para a forma original, resultando em uma lei de potência.
    
    Args:
        x_medidas (np.ndarray): Array de medidas da variável independente.
        y_medidas (np.ndarray): Array de medidas da variável dependente.
    
    Raises:
        ValueError: Se x_medidas contiver valores negativos ou zero.
        ValueError: Se y_medidas contiver valores negativos ou zero.
        ValueError: Se `x_medidas` e `y_medidas` não tiverem o mesmo tamanho 
    
    Returns:
        MLeiDePotencia: Objeto contendo os coeficientes da lei de potência ajustada.
    """

    log_y_medidas=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(y_medidas,log)
    log_x_medidas=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(x_medidas,log)
    polinomio=regressao_linear(log_x_medidas,log_y_medidas)
    a=_aplicar_funcao_sem_passar_pelo_sistema_de_unidades(np.array([polinomio.b]),exp)[0]
    n=polinomio.a
    a=_forcar_troca_de_unidade(np.array([a]),str((y_medidas[0]._nominal/x_medidas[0]._nominal**n._nominal.magnitude).units))
    n=_forcar_troca_de_unidade(np.array([n]),"dimensionless")
    return MLeiDePotencia(a[0],n[0],y_medidas[0]._nominal)