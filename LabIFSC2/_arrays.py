from collections.abc import Iterable
from numbers import Real

import numpy as np
from numpy.typing import NDArray

from ._medida import Medida
from ._regressoes import Regressao


def nominais(medidas: Iterable[Medida], unidade: str) -> NDArray[np.float64]:
    """
    Converte um iterável de objetos Medida para um array de valores nominais em uma unidade especificada.

    Args:
        medidas (Iterable[Medida]): Iterável de objetos Medida.
        unidade (str): Unidade para a conversão dos valores nominais. Use 'si' para unidades do Sistema Internacional.

    Returns:
        np.ndarray: Array de valores nominais convertidos para a unidade especificada.

    Raises:
        TypeError: Se algum dos valores não for um objeto Medida.
    """
    try:
        if unidade == "si":
            return np.array(
                [medida._nominal.to_base_units().magnitude for medida in medidas],
                dtype=float,
            )
        else:
            return np.array(
                [medida._nominal.to(unidade).magnitude for medida in medidas],
                dtype=float,
            )
    except AttributeError as e:
        raise TypeError("Os valores do array não são Medidas") from e


def incertezas(medidas: Iterable[Medida], unidade: str) -> NDArray[np.float64]:
    """
    Converte um iterável de objetos Medida para um array de incertezas em uma unidade especificada.

    Args:
        medidas (Iterable[Medida]): Iterável de objetos Medida.
        unidade (str): Unidade para a conversão das incertezas. Use 'si' para unidades do Sistema Internacional.

    Returns:
        np.ndarray: Array de incertezas convertidas para a unidade especificada.

    Raises:
        TypeError: Se algum dos valores não for um objeto Medida.
    """
    try:
        if unidade == "si":
            return np.array(
                [medida._incerteza.to_base_units().magnitude for medida in medidas],
                dtype=float,
            )
        else:
            return np.array(
                [medida._incerteza.to(unidade).magnitude for medida in medidas],
                dtype=float,
            )
    except AttributeError as e:
        raise TypeError("Os valores do array não são Medidas") from e


def _curva_min_max(
    medidas: Iterable[Medida] | Regressao, op: str, unidade_y: str, sigmas: float
) -> NDArray[np.float64]:
    if sigmas <= 0:
        raise ValueError("O número de sigmas deve ser positivo")

    if not isinstance(medidas, Regressao):
        if op == "min":
            minima: NDArray[np.float64] = nominais(
                medidas, unidade_y
            ) - sigmas * incertezas(medidas, unidade_y)
            return minima
        elif op == "max":
            maxima: NDArray[np.float64] = nominais(
                medidas, unidade_y
            ) + sigmas * incertezas(medidas, unidade_y)
            return maxima
    else:
        if medidas._amostragem_pre_calculada is None:
            raise ValueError("A regressão não amostrada ainda")
        elif op == "min":
            resultado_min: NDArray[np.float64] = nominais(
                medidas._amostragem_pre_calculada, unidade_y
            ) - sigmas * incertezas(medidas._amostragem_pre_calculada, unidade_y)
            return resultado_min
        elif op == "max":
            resultado_max: NDArray[np.float64] = nominais(
                medidas._amostragem_pre_calculada, unidade_y
            ) + sigmas * incertezas(medidas._amostragem_pre_calculada, unidade_y)
            return resultado_max
    return np.array([], dtype=np.float64)


def curva_min(
    medidas: Iterable[Medida] | Regressao, unidade_y: str, sigmas: float = 2
) -> NDArray[np.float64]:
    """
    Calcula a curva mínima de uma série de medidas.

    Args:
        medidas (Iterable[Medida] | Regressao): Iterável de objetos Medida ou objeto Regressao.
        unidade_y (str): Unidade da variável dependente.
        sigmas (float): Número de sigmas para a curva mínima.

    Returns:
        np.ndarray: Array de valores da curva mínima.
    """
    resultado: NDArray[np.float64] = _curva_min_max(medidas, "min", unidade_y, sigmas)
    return resultado


def curva_max(
    medidas: Iterable[Medida] | Regressao, unidade_y: str, sigmas: float = 2
) -> NDArray[np.float64]:
    """
    Calcula a curva máxima de uma série de medidas.

    Args:
        medidas (Iterable[Medida] | Regressao): Iterável de objetos Medida ou objeto Regressao.
        unidade_y (str): Unidade da variável dependente.
        sigmas (float): Número de sigmas para a curva máxima.

    Returns:
        np.ndarray: Array de valores da curva máxima.
    """
    resultado: NDArray[np.float64] = _curva_min_max(medidas, "max", unidade_y, sigmas)
    return resultado


def linspaceM(
    a: float, b: float, n: int, unidade: str, incertezas: float
) -> NDArray[np.object_]:
    """Gera um array de Medidas com valores igualmente espaçados, seguindo as convenções
    da função np.linpsace do NumPy.

    Args:
        a (float): O valor inicial do intervalo.
        b (float): O valor final do intervalo.
        n (int): O número de elementos no array.
        unidade (str): A unidade das medidas.
        incertezas (float): A incerteza associada a cada medida.

    Returns:
        np.ndarray: Um array de objetos Medida com valores igualmente espaçados.
    """
    return np.array(
        [Medida(i, unidade, incertezas) for i in np.linspace(a, b, n)], dtype=object
    )


def arrayM(
    valores: Iterable[float], unidade: str, incerteza: float
) -> NDArray[np.object_]:
    """
    Cria um array de objetos Medida a partir de valores nominais, unidade e incerteza.

    Args:
        valores (Iterable[float]): Um iterável de valores nominais.
        unidade (str): A unidade de medida.
        incerteza (float): A incerteza associada aos valores nominais.

    Returns:
        np.ndarray: Um array de objetos Medida.

    Raises:
        TypeError: Se os valores não forem números reais.
    """
    resultados: list[Medida] = []
    for nominal in valores:
        if not isinstance(nominal, Real):
            raise TypeError("Os valores do array não são números reais")
        resultados.append(Medida(nominal, unidade, incerteza))
    return np.array(resultados, dtype=Medida)
