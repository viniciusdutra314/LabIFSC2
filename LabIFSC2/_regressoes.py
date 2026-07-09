import string
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import cast
from numpy.typing import NDArray

import numpy as np
import pint
from numpy import  log, power
from numpy.polynomial import Polynomial

from ._medida import Medida


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


class Regressao(ABC):

    def __init__(self) -> None:
        self._amostragem_pre_calculada: NDArray[np.object_] | None = None
        self._valores: Iterator[object] = iter([])

    def _retornar(self, y: NDArray[np.object_], unidade_y: str) -> NDArray[np.float64]:
        for y_medida in y:
            cast(Medida, y_medida)._histograma = None
        self._amostragem_pre_calculada = y

        resultado: NDArray[np.float64] = np.array(
            [cast(Medida, x).nominal(unidade_y) for x in self._amostragem_pre_calculada], dtype=float)
        return resultado

    def _verificar_tipo_de_x(self, x: NDArray[np.object_]) -> None:
        if not isinstance(x[0], Medida):
            raise TypeError("x precisa ser um array de medidas ou uma medida \
mesmo que com incerteza 0, pois precisamos das unidades")
        return None

    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def amostrar(self, x: NDArray[np.object_], unidade_y: str) -> NDArray[np.float64]: ...

    def __iter__(self) -> Iterator[object]:
        return self._valores


class MPolinomio(Regressao):

    def __init__(self, coeficientes: Iterable[Medida]):
        super().__init__()
        self._coeficientes: list[Medida] = [coef for coef in coeficientes]
        self.grau = len(self._coeficientes)-1

    def __getattr__(self, name: str) -> Medida:
        if name in string.ascii_lowercase:
            index = string.ascii_lowercase.index(name)
            if index <= self.grau:
                return self._coeficientes[index]
        raise AttributeError(f"'MPolinomio' object has no attribute '{name}'")

    def amostrar(self: 'MPolinomio', x: NDArray[np.object_], unidade_y: str) -> NDArray[np.float64]:
        """
        Calcula os valores de um polinômio para um conjunto de entradas x.

        Args:
            x (NDArray[np.object_]): Um array de valores nos quais o polinômio será avaliado.
            unidade_y (str): A unidade de medida para os valores calculados do polinômio.

        Returns:
            NDArray[np.float64]: Um array contendo os valores calculados do polinômio nas unidades especificadas.

        Raises:
            TypeError: Se o tipo de ``x`` não for um array de Medida.
        """

        self._verificar_tipo_de_x(x)
        y: Medida | NDArray[np.object_] = Medida(0, unidade_y, 0)
        for index, coef in enumerate(self._coeficientes):
            y += power(x, self.grau-index)*coef
        polinomio_calculado: NDArray[np.object_] = cast(NDArray[np.object_], y)
        return self._retornar(polinomio_calculado, unidade_y)

    def __iter__(self) -> Iterator[Medida]:
        return iter(self._coeficientes)

    def __repr__(self) -> str:
        return f"MPolinomio(coefs={self._coeficientes},grau={self.grau})"


class MExponencial(Regressao):
    '''Classe para modelar uma função exponencial
    y = a * base^(kx)
    '''
    __slots__ = ['cte_multiplicativa', 'expoente', 'base', '_valores']

    def __init__(self, a: Medida, k: Medida, base: float):
        super().__init__()
        self.cte_multiplicativa = a
        self.base = base
        self.expoente = k
        self._valores = iter((a, k, base))

    def amostrar(self: 'MExponencial', x: NDArray[np.object_], unidade_y: str) -> NDArray[np.float64]:
        """
        Gera uma amostra de valores exponenciais com base nos parâmetros fornecidos.

        Args:
            x (NDArray[np.object_]): Um array de valores de entrada.
            unidade_y (str): A unidade dos valores de saída.

        Returns:
            NDArray[np.float64]: Um array de valores calculados com base na função exponencial.

        Raises:
            TypeError: Se o tipo de ``x`` não for um array de Medida.
        """

        self._verificar_tipo_de_x(x)
        y: NDArray[np.object_] = np.power(
            float(self.base), (self.expoente*x))*self.cte_multiplicativa
        return self._retornar(y, unidade_y)

    def __repr__(self) -> str:
        return f'MExponencial(cte_multiplicativa={self.cte_multiplicativa},expoente={self.expoente},base={self.base})'


class MLeiDePotencia(Regressao):

    def __init__(self, a: Medida, n: Medida, y_unidade: pint.Quantity[float] | str):
        super().__init__()
        self.cte_multiplicativa = a
        self.potencia = n
        self._valores = iter([a, n])
        self._y_unidade = y_unidade

    def amostrar(self: 'MLeiDePotencia', x: NDArray[np.object_], unidade_y: str) -> NDArray[np.float64]:
        """
        Amostra valores baseados na lei de potência.

        Args:
            x (NDArray[np.object_]): Array de valores de entrada.
            unidade_y (str): Unidade da variável dependente y.

        Returns:
            NDArray[np.float64]: Array de valores amostrados com a unidade especificada.

        Raises:
            ValueError: Se a unidade de x não for compatível com a unidade esperada.
        """

        self._verificar_tipo_de_x(x)
        unidade_expoente = str((cast(Medida, x[0])._nominal**self.potencia._nominal).units)
        x = _forcar_troca_de_unidade(x, '')
        expoente = x**self.potencia
        expoente_medida = _forcar_troca_de_unidade(expoente, unidade_expoente)
        y: NDArray[np.object_] = expoente_medida*self.cte_multiplicativa
        if not cast(Medida, y[0])._nominal.is_compatible_with(self._y_unidade):
            raise ValueError(f'Unidade de x não está correta')
        return self._retornar(y, unidade_y)

    def __repr__(self) -> str:
        return f'MLeiDePotencia(cte_multiplicativa={self.cte_multiplicativa}, potencia={self.potencia})'


def regressao_polinomial(x_medidas: Sequence[Medida], y_medidas: Sequence[Medida], grau: int) -> MPolinomio:
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
        TypeError: Se ``x_medidas`` e ``y_medidas`` não forem sequências de medidas.
    """

    if len(x_medidas) != len(y_medidas):
        raise ValueError("x_dados e y_dados não tem o mesmo tamanho")
    if len(x_medidas) <= grau+1:
        raise ValueError(
            f"Não há dados suficientes para um polinômio de grau {grau} (overfitting)")
    if not (isinstance(x_medidas[0], Medida) and isinstance(y_medidas[0], Medida)):
        raise TypeError(
            'x_medidas e y_medidas precisam ser sequências de medidas')
    x_float = np.array([x._nominal.magnitude for x in x_medidas], dtype=float)
    y_float = np.array([y._nominal.magnitude for y in y_medidas], dtype=float)
    p, cov = np.polyfit(x_float, y_float, grau, cov=True)
    erros = np.sqrt(np.diag(cov))
    medidas_coeficientes = []
    for index in range(len(p)):
        unidade = str(
            (y_medidas[0]._nominal/x_medidas[0]._nominal**(grau-index)).units)
        medidas_coeficientes.append(Medida(p[index], unidade, erros[index]))
    return MPolinomio(medidas_coeficientes)


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
