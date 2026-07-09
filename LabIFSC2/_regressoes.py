import string
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import cast
from numpy.typing import NDArray
from typing import NamedTuple
import numpy as np
import pint
from numpy import  log, power
from numpy.polynomial import Polynomial

from ._medida import Medida

'''
Resultado de um ajuste exponencial da forma
y = amplitude * exp(exponente * x)
'''
class AjusteExponencial(NamedTuple):
    amplitude: Medida
    expoente: Medida
    def __call__(self,medidas:Medida | Sequence[Medida])-> Medida | NDArray[np.object_]:
        if isinstance(medidas,Medida):
            return self.amplitude * ((self.expoente * medidas).exp())
        else:
            return np.array(
                [self.amplitude * ((self.expoente * medida).exp()) for medida in medidas],
                dtype=object)

'''
Resultado de um ajuste de lei de potência na forma
y = amplitude * x ^ potencia
'''
class AjusteLeiDePotencia(NamedTuple):
    amplitude: Medida
    potencia: Medida
    def __call__(self,medidas:Medida | Sequence[Medida])-> Medida | NDArray[np.object_]:
        if isinstance(medidas,Medida):
            return self.amplitude * (medidas**self.potencia)
        else:
            return np.array(
                [self.amplitude * (medida**self.potencia) for medida in medidas],
                dtype=object)
'''
Resultado de um ajuste linear da forma
y = ax + b
'''
class AjusteLinear(NamedTuple):
    a:Medida
    b:Medida
    def __call__(self,medidas:Medida | Sequence[Medida])-> Medida | NDArray[np.object_]:
        if isinstance(medidas,Medida):
            return self.a * medidas+self.b
        else:
            return np.array(
                [self.a * medida +self.b for medida in medidas],
                dtype=object)
'''
Resultado de um ajuste quadrático da forma
y = ax² + bx + c 
'''
class AjusteQuadratico(NamedTuple):
    a:Medida
    b:Medida
    c:Medida
    def __call__(self,medidas:Medida | Sequence[Medida])-> Medida | NDArray[np.object_]:
        if isinstance(medidas,Medida):
            return self.a * (medidas**2) +self.b*medidas + self.c
        else:
            return np.array(
                [self.a * (medida**2) +self.b*medida + self.c for medida in medidas],
                dtype=object)
class AjustePolinomial:
    """
    Resultado de um ajuste polinomial genérico da forma:
    y = coef[0] + coef[1]*x + coef[2]*x^2 + ... + coef[n]*x^n
    """
    def __init__(self, coeficientes: Sequence[Medida]):
        self.coef = coeficientes
        self.grau = len(coeficientes) - 1
        
    def __repr__(self) -> str:
        return f"AjustePolinomial(grau={self.grau}, coeficientes={self.coef})"
    def __call__(self,medidas:Medida | Sequence[Medida])-> Medida | NDArray[np.object_]:
        
        if isinstance(medidas,Medida):
            zero=medidas-medidas
            return sum([coef * (medidas**i) for i, coef in enumerate(self.coef)],start=zero)
        else:
            
            return np.array(
                [sum([coef * (medida**i) for i, coef in enumerate(self.coef)]) for medida in medidas],
                dtype=object)

def _aplicar_funcao_sem_passar_pelo_sistema_de_unidades(
        array_medidas: Iterable[Medida], lab_func: Callable[[Medida], Medida]) -> list[Medida]:
    '''
    precisamos aplicar log/exp sem passar pelo sistema de unidades
    um método meio quicky and dirty mas necessário para não dar erro de dimensão
    '''
    medidas_novas = []
    for medida in array_medidas:
        unidade = str(medida._nominal.units)
        medida_intermediaria = Medida(
            medida._nominal.magnitude, "", medida._incerteza._magnitude)
        medida_intermediaria = lab_func(medida_intermediaria)
        nominal = medida_intermediaria._nominal._magnitude
        incerteza = medida_intermediaria._incerteza._magnitude
        if np.isnan(nominal) or np.isnan(incerteza):
            raise ValueError(f'Erro ao aplicar {lab_func} no processo de regressão. Lembre-se que, para regressões \
exponenciais, todos os valores de y precisam ser positivos. No caso da regressão de lei de potência, os valores \
em x também precisam ser positivos. Além disso, um valor pode não ser negativo, mas devido à incerteza associada, ele pode assumir valores negativos.')
        medidas_novas.append(Medida(nominal, unidade, incerteza))
    return medidas_novas


def _forcar_troca_de_unidade(medidas: Iterable[Medida], unidade: str) -> NDArray[np.object_]:
    return np.array([Medida(med._nominal.magnitude, unidade, med._incerteza.magnitude,) for med in medidas])



def regressao_polinomial(x_medidas: Sequence[Medida], 
                         y_medidas: Sequence[Medida], 
                         grau: int) -> AjustePolinomial:
    """
    Realiza uma regressão polinomial nos dados fornecidos.

    Args:
        x_medidas (Sequence[Medida]): Sequência de medidas para a variável independente.
        y_medidas (Sequence[Medida]): Sequência de medidas para a variável dependente.
        grau (int): Grau do polinômio a ser ajustado.

    Returns:
        MPolinomio: Um objeto representando o polinômio ajustado com coeficientes como medidas.

    Raises:
        ValueError: Se ``x_medidas`` e ``y_medidas`` não tiverem o mesmo tamanho ou se não houver dados 
        suficientes para o grau do polinômio.
    """

    if len(x_medidas) != len(y_medidas):
        raise ValueError("x_dados e y_dados não tem o mesmo tamanho")
    if len(x_medidas) <= grau+1:
        raise ValueError(
            f"Não há dados suficientes para um polinômio de grau {grau} (overfitting)")
    x_float = np.array([x._nominal.magnitude for x in x_medidas], dtype=float)
    y_float = np.array([y._nominal.magnitude for y in y_medidas], dtype=float)
    p, cov = np.polyfit(x_float, y_float, grau, cov=True)
    erros = np.sqrt(np.diag(cov))
    coefs:list[Medida] = []
    for index in range(len(p)):
        unidade = str(
            (y_medidas[0]._nominal/x_medidas[0]._nominal**(grau-index)).units)
        coefs.append(Medida(p[index], unidade, erros[index]))
    return AjustePolinomial(coefs)


def regressao_linear(x_medidas: Sequence[Medida],
                     y_medidas: Sequence[Medida]) -> MPolinomio:
    """
    Calcula a regressão linear para um conjunto de medidas.

    Args:
        x_medidas (Sequence[Medida]): Sequência contendo as medidas da variável independente.
        y_medidas (Sequence[Medida]): Sequência contendo as medidas da variável dependente.

    Raises:
        ValueError: Se ``x_medidas`` e ``y_medidas`` não tiverem o mesmo tamanho.

    Returns:
        MPolinomio: Objeto representando a reta de regressão linear ajustada aos dados.
    """
    reta: MPolinomio = regressao_polinomial(x_medidas, y_medidas, 1)
    return reta


def regressao_exponencial(x_medidas: Sequence[Medida], y_medidas: Sequence[Medida],
                          base: float = np.exp(1)) -> MExponencial:
    """
    y=ae^{kx}
    Realiza uma regressão exponencial nos dados fornecidos.

    Args:
        x_medidas (Sequence[Medida]): Sequência de medidas da variável independente.
        y_medidas (Sequence[Medida]): Sequência de medidas da variável dependente.
        base (float, opcional): Base da exponencial usada, o padrão é o número de Euler (e).

    Raises:
        ValueError: Se a base for menor que 1.
        ValueError: Se y_medidas contiver valores negativos ou zero.
        ValueError: Se ``x_medidas`` e ``y_medidas`` não tiverem o mesmo tamanho.

    Returns:
        MExponencial: Objeto contendo os parâmetros ``a`` e ``k`` da regressão exponencial e a base utilizada.
    """
    if any(y._nominal.magnitude <= 0 for y in y_medidas):
        raise ValueError(
            'Todos os valores de y_medidas devem ser positivos e não nulos para a regressão exponencial.')
    if base < 1:
        raise ValueError('Base precisa ser maior que 1')

    def pegar_log(x: Medida) -> Medida: return x.log()/float(log(float(base)))
    log_y_medidas = _aplicar_funcao_sem_passar_pelo_sistema_de_unidades(
        y_medidas, pegar_log)
    polinomio = regressao_linear(x_medidas, log_y_medidas)
    k_coef = polinomio.a
    a_medida = _aplicar_funcao_sem_passar_pelo_sistema_de_unidades(
        np.array([polinomio.b]), lambda val: val.exp())[0]
    k = _forcar_troca_de_unidade(
        [k_coef], str((1/x_medidas[0]._nominal).units))
    a_arr = _forcar_troca_de_unidade([a_medida], str(y_medidas[0]._nominal.units))
    return MExponencial(a_arr[0], k[0], base)


def regressao_potencia(x_medidas: Sequence[Medida], y_medidas: Sequence[Medida]) -> MLeiDePotencia:
    """
    y=a*x^n

    Realiza uma regressão de potência nos dados fornecidos.
    Esta função aplica uma transformação logarítmica aos dados de entrada, realiza uma regressão linear nos dados transformados,
    e então converte os coeficientes da regressão linear de volta para a forma original, resultando em uma lei de potência.

    Args:
        x_medidas (Sequence[Medida]): Sequência de medidas da variável independente.
        y_medidas (Sequence[Medida]): Sequência de medidas da variável dependente.

    Raises:
        ValueError: Se x_medidas contiver valores negativos ou zero.
        ValueError: Se y_medidas contiver valores negativos ou zero.
        ValueError: Se ``x_medidas`` e ``y_medidas`` não tiverem o mesmo tamanho.

    Returns:
        MLeiDePotencia: Objeto contendo os coeficientes da lei de potência ajustada.
    """

    log_y_medidas = _aplicar_funcao_sem_passar_pelo_sistema_de_unidades(
        y_medidas, lambda val: val.log())
    log_x_medidas = _aplicar_funcao_sem_passar_pelo_sistema_de_unidades(
        x_medidas, lambda val: val.log())
    polinomio = regressao_linear(log_x_medidas, log_y_medidas)
    a_medida = _aplicar_funcao_sem_passar_pelo_sistema_de_unidades(
        np.array([polinomio.b]), lambda val: val.exp())[0]
    n_coef = polinomio.a
    a_arr = _forcar_troca_de_unidade(np.array([a_medida]), str(
        (y_medidas[0]._nominal/x_medidas[0]._nominal**n_coef._nominal.magnitude).units))
    n = _forcar_troca_de_unidade([n_coef], "dimensionless")
    return MLeiDePotencia(a_arr[0], n[0], cast(pint.Quantity[float], y_medidas[0]._nominal))
