from collections.abc import Iterable
from numbers import Real

import numpy as np
from numpy.typing import NDArray

from ._medida import Medida


def nominais(medidas: Iterable[Medida], unidade: str) -> NDArray[np.float64]:
    """
    Converte um iterável de objetos Medida para um array de valores nominais em uma unidade especificada.

    Args:
        medidas (Iterable[Medida]): Iterável de objetos Medida.
        unidade (str): Unidade para a conversão dos valores nominais. Use 'si' para unidades do Sistema Internacional.

    Returns:
        NDArray[np.float64]: Array de valores nominais convertidos para a unidade especificada.

    Raises:
        TypeError: Se algum dos valores não for um objeto Medida.
    """
    try:
        return np.array(
            [medida.nominal(unidade) for medida in medidas],
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
        NDArray[np.float64]: Array de incertezas convertidas para a unidade especificada.

    Raises:
        TypeError: Se algum dos valores não for um objeto Medida.
    """
    try:
        return np.array(
            [medida.incerteza(unidade) for medida in medidas],
            dtype=float,
        )
    except AttributeError as e:
        raise TypeError("Os valores do array não são Medidas") from e

def curva_min(
    medidas: Iterable[Medida], unidade_y: str, sigmas: float = 2
) -> NDArray[np.float64]:
    """
    Calcula a curva mínima de uma série de medidas.

    Para usar com um ajuste, passe o resultado de ``ajuste(x_array)`` como argumento.

    Args:
        medidas (Iterable[Medida]): Iterável de objetos Medida (e.g. saída de um Ajuste chamável).
        unidade_y (str): Unidade da variável dependente.
        sigmas (float): Número de sigmas para a curva mínima.

    Returns:
        NDArray[np.float64]: Array de valores da curva mínima.
    """
    if sigmas <= 0:
        raise ValueError("O número de sigmas deve ser positivo")
    return nominais(medidas, unidade_y) - sigmas * incertezas(medidas, unidade_y)


def curva_max(
    medidas: Iterable[Medida], unidade_y: str, sigmas: float = 2
) -> NDArray[np.float64]:
    """
    Calcula a curva máxima de uma série de medidas.

    Para usar com um ajuste, passe o resultado de ``ajuste(x_array)`` como argumento.

    Args:
        medidas (Iterable[Medida]): Iterável de objetos Medida (e.g. saída de um Ajuste chamável).
        unidade_y (str): Unidade da variável dependente.
        sigmas (float): Número de sigmas para a curva máxima.

    Returns:
        NDArray[np.float64]: Array de valores da curva máxima.
    """
    if sigmas <= 0:
        raise ValueError("O número de sigmas deve ser positivo")
    return nominais(medidas, unidade_y) + sigmas * incertezas(medidas, unidade_y)

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
        NDArray[np.object_]: Um array de objetos Medida com valores igualmente espaçados.
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
        NDArray[np.object_]: Um array de objetos Medida.
    """
    resultados: list[Medida] = []
    for nominal in valores:
        if not isinstance(nominal, Real):
            raise TypeError("Os valores do array não são números reais")
        resultados.append(Medida(nominal, unidade, incerteza))
    return np.array(resultados, dtype=Medida)
