from collections.abc import Sequence
from typing import NamedTuple
import numpy as np
from numpy.typing import NDArray

from ._medida import Medida, ureg


def _obter_unidade_si(medida: Medida) -> str:
    dim = medida.dimensao
    if not dim:
        return ""
    MAP_DIMENSOES_SI = {
        '[length]': 'meter',
        '[time]': 'second',
        '[mass]': 'kilogram',
        '[current]': 'ampere',
        '[temperature]': 'kelvin',
        '[amount]': 'mole',
        '[luminosity]': 'candela',
    }
    units_dict = {MAP_DIMENSOES_SI.get(k, k): v for k, v in dim.items()}
    uc = ureg.UnitsContainer(units_dict)
    return str(ureg.Unit(uc))


'''
Resultado de um ajuste exponencial da forma
y = amplitude * exp(expoente * x)
'''
class AjusteExponencial(NamedTuple):
    amplitude: Medida
    expoente: Medida
    def __call__(self, medidas: Medida | Sequence[Medida]) -> Medida | NDArray[np.object_]:
        if isinstance(medidas, Medida):
            return self.amplitude * ((self.expoente * medidas).exp())
        else:
            return np.array(
                [self.amplitude * ((self.expoente * medida).exp()) for medida in medidas],
                dtype=object)
    def __repr__(self) -> str:
        return f'AjusteExponencial(amplitude={self.amplitude}, expoente={self.expoente})'


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
y = a*x + b
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
y = a*x² + b*x + c
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
                [self.a * (medida ** 2) + self.b * medida + self.c for medida in medidas],
                dtype=object)
class AjustePolinomial:
    """
    Resultado de um ajuste polinomial genérico da forma:
    y = coef[0] + coef[1]*x + coef[2]*x^2 + ... + coef[n]*x^n
    """

    def __init__(self, coeficientes: Sequence[Medida]) -> None:
        self.coef = list(coeficientes)
        self.grau = len(self.coef) - 1

    def __iter__(self):
        # Itera em ordem decrescente de grau (coef[n], ..., coef[0])
        return iter(reversed(self.coef))

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



def _validar_medidas(x: Sequence[Medida], y: Sequence[Medida], *, positivos_x: bool = False, positivos_y: bool = False) -> None:
    if len(x) == 0 or len(y) == 0:
        raise ValueError("x_medidas e y_medidas não podem ser vazios")
    if len(x) != len(y):
        raise ValueError("x_dados e y_dados não tem o mesmo tamanho")
    if not (isinstance(x[0], Medida) and isinstance(y[0], Medida)):
        raise TypeError("x_medidas e y_medidas precisam ser sequências de Medida")
    if positivos_x and any(m.nominal('si') <= 0 for m in x):
        raise ValueError(
            "Todos os valores de x_medidas devem ser positivos e não nulos.")
    if positivos_y and any(m.nominal('si') <= 0 for m in y):
        raise ValueError(
            "Todos os valores de y_medidas devem ser positivos e não nulos.")


def _polifit_com_medidas(x: Sequence[Medida], y: Sequence[Medida], grau: int,
             unidade_x: str, unidade_y: str) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    p, cov = np.polyfit([m.nominal(unidade_x) for m in x], [m.nominal(unidade_y) for m in y], grau, cov=True)
    erros = np.sqrt(np.diag(cov))
    # Retorna em ordem crescente de grau (coef[0] acompanha x^0, coef[grau] acompanha x^grau)
    return p[::-1], erros[::-1]


def regressao_polinomial(x_medidas: Sequence[Medida], 
                         y_medidas: Sequence[Medida], 
                         grau: int) -> AjustePolinomial:
    """
    Realiza uma regressão polinomial nos dados fornecidos.

    A regressão ajusta um polinômio de grau ``grau`` da forma:
    y = coef[0] + coef[1]*x + ... + coef[grau]*x^grau

    Args:
        x_medidas (Sequence[Medida]): Sequência de medidas para a variável independente.
        y_medidas (Sequence[Medida]): Sequência de medidas para a variável dependente.
        grau (int): Grau do polinômio a ser ajustado.

    Returns:
        AjustePolinomial: Objeto representando o polinômio ajustado com coeficientes como Medidas.

    Raises:
        TypeError: Se x_medidas ou y_medidas não forem sequências de Medida.
        ValueError: Se x_medidas e y_medidas não tiverem o mesmo tamanho.
        ValueError: Se não houver dados suficientes para o grau do polinômio (overfitting).
    """
    _validar_medidas(x_medidas, y_medidas)
    if len(x_medidas) <= grau + 1:
        raise ValueError(
            f"Não há dados suficientes para um polinômio de grau {grau} (overfitting)")
    p, erros = _polifit_com_medidas(x_medidas, y_medidas, grau, "si", "si")
    unidade_x_si = _obter_unidade_si(x_medidas[0])
    unidade_y_si = _obter_unidade_si(y_medidas[0])
    coefs: list[Medida] = []
    for i in range(grau + 1):
        unidade_coef = _obter_unidade_si(Medida(1.0, unidade_y_si) / Medida(1.0, unidade_x_si) ** i)
        coefs.append(Medida(float(p[i]), unidade_coef, float(erros[i])))

    return AjustePolinomial(coefs)


def regressao_linear(x_medidas: Sequence[Medida],
                     y_medidas: Sequence[Medida]) -> AjusteLinear:
    """
    Calcula a regressão linear para um conjunto de medidas.

    Ajusta uma reta da forma y = a*x + b.

    Args:
        x_medidas (Sequence[Medida]): Sequência contendo as medidas da variável independente.
        y_medidas (Sequence[Medida]): Sequência contendo as medidas da variável dependente.

    Returns:
        AjusteLinear: Objeto representando a reta de regressão linear ajustada aos dados.

    Raises:
        TypeError: Se x_medidas ou y_medidas não forem sequências de Medida.
        ValueError: Se x_medidas e y_medidas não tiverem o mesmo tamanho.
    """
    _validar_medidas(x_medidas, y_medidas)
    polinomio = regressao_polinomial(x_medidas, y_medidas, 1)
    b = polinomio.coef[0]
    a = polinomio.coef[1]
    return AjusteLinear(a, b)


def regressao_quadratica(x_medidas: Sequence[Medida],
                         y_medidas: Sequence[Medida]) -> AjusteQuadratico:
    """
    Calcula a regressão quadrática para um conjunto de medidas.

    Ajusta uma parábola da forma y = a*x² + b*x + c.

    Args:
        x_medidas (Sequence[Medida]): Sequência contendo as medidas da variável independente.
        y_medidas (Sequence[Medida]): Sequência contendo as medidas da variável dependente.

    Returns:
        AjusteQuadratico: Objeto representando a parábola de regressão quadrática ajustada aos dados.

    Raises:
        TypeError: Se x_medidas ou y_medidas não forem sequências de Medida.
        ValueError: Se x_medidas e y_medidas não tiverem o mesmo tamanho.
        ValueError: Se não houver dados suficientes para o ajuste.
    """
    _validar_medidas(x_medidas, y_medidas)
    polinomio = regressao_polinomial(x_medidas, y_medidas, 2)
    c = polinomio.coef[0]
    b = polinomio.coef[1]
    a = polinomio.coef[2]
    return AjusteQuadratico(a, b, c)


def regressao_exponencial(x_medidas: Sequence[Medida],
                          y_medidas: Sequence[Medida],
                          base: float = np.e) -> AjusteExponencial:
    """
    Realiza uma regressão exponencial nos dados fornecidos.

    Ajusta uma curva da forma y = amplitude * base^(expoente * x).
    A linearização é feita via log_base(y) = log_base(amplitude) + expoente * x.

    Args:
        x_medidas (Sequence[Medida]): Sequência de medidas da variável independente.
        y_medidas (Sequence[Medida]): Sequência de medidas da variável dependente (todos positivos).
        base (float, opcional): Base da exponencial usada, o padrão é o número de Euler (e).

    Returns:
        AjusteExponencial: Objeto contendo amplitude e expoente da regressão exponencial.

    Raises:
        TypeError: Se x_medidas ou y_medidas não forem sequências de Medida.
        ValueError: Se base < 1.
        ValueError: Se y_medidas contiver valores não-positivos.
        ValueError: Se x_medidas e y_medidas não tiverem o mesmo tamanho.
    """
    _validar_medidas(x_medidas, y_medidas, positivos_y=True)
    if base < 1:
        raise ValueError('Base precisa ser maior que 1')

    unidade_x_si = _obter_unidade_si(x_medidas[0])
    unidade_y_si = _obter_unidade_si(y_medidas[0])

    x_float = np.array([m.nominal("si") for m in x_medidas], dtype=float)
    y_float = np.array([m.nominal("si") for m in y_medidas], dtype=float)
    log_y = np.log(y_float) / np.log(base)

    p, cov = np.polyfit(x_float, log_y, 1, cov=True)
    erros = np.sqrt(np.diag(cov))
    unidade_expoente = _obter_unidade_si(1 / Medida(1.0, unidade_x_si))
    k = Medida(float(p[0]), unidade_expoente, float(erros[0]))

    a_val = float(base ** p[1])
    a_err = abs(a_val * np.log(base) * erros[1])
    a = Medida(a_val, unidade_y_si, a_err)
    return AjusteExponencial(a, k)


def regressao_potencia(x_medidas: Sequence[Medida],
                       y_medidas: Sequence[Medida]) -> AjusteLeiDePotencia:
    """
    Realiza uma regressão de lei de potência nos dados fornecidos.

    Ajusta uma curva da forma y = amplitude * x^potencia.
    A linearização é feita via log(y) = log(amplitude) + potencia * log(x).

    Args:
        x_medidas (Sequence[Medida]): Sequência de medidas da variável independente (todos positivos).
        y_medidas (Sequence[Medida]): Sequência de medidas da variável dependente (todos positivos).

    Returns:
        AjusteLeiDePotencia: Objeto contendo amplitude e potência da regressão.

    Raises:
        TypeError: Se x_medidas ou y_medidas não forem sequências de Medida.
        ValueError: Se x_medidas ou y_medidas contiverem valores não-positivos.
        ValueError: Se x_medidas e y_medidas não tiverem o mesmo tamanho.
    """
    _validar_medidas(x_medidas, y_medidas, positivos_x=True, positivos_y=True)

    unidade_x_si = _obter_unidade_si(x_medidas[0])
    unidade_y_si = _obter_unidade_si(y_medidas[0])

    x_float = np.array([m.nominal("si") for m in x_medidas], dtype=float)
    y_float = np.array([m.nominal("si") for m in y_medidas], dtype=float)
    log_x = np.log(x_float)
    log_y = np.log(y_float)

    p, cov = np.polyfit(log_x, log_y, 1, cov=True)
    erros = np.sqrt(np.diag(cov))

    n_val = float(p[0])
    n = Medida(n_val, '', float(erros[0]))
    a_val = float(np.exp(p[1]))
    a_err = abs(a_val * erros[1])
    a = Medida(a_val, unidade_y_si, a_err)
    return AjusteLeiDePotencia(a, n, unidade_x_si, unidade_y_si)
