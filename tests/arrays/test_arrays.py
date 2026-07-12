from collections.abc import Callable, Iterable

import numpy as np
import pytest
from numpy.typing import NDArray

from LabIFSC2 import (
    AjustePolinomial,
    Medida,
    arrayM,
    curva_max,
    curva_min,
    incertezas,
    linspaceM,
    nominais,
    regressao_linear,
)
from tests.utilities import assert_array_proximo, assert_medida_proxima


@pytest.fixture
def valores_nominais() -> list[float]:
    return [13431, 0.006132, -34, -5313.351, 0]


@pytest.fixture
def medidas_nominais(valores_nominais: list[float]) -> list[Medida]:
    return [Medida(valor, "", 1) for valor in valores_nominais]


@pytest.fixture
def medidas_em_centimetros(valores_nominais: list[float]) -> list[Medida]:
    return [Medida(valor, "cm", 1) for valor in valores_nominais]


def test_nominais(
    medidas_nominais: list[Medida], valores_nominais: list[float]
) -> None:
    assert_array_proximo(nominais(medidas_nominais, ""), valores_nominais, rtol=0)


def test_nominais_convertem_para_si(
    medidas_em_centimetros: list[Medida], valores_nominais: list[float]
) -> None:
    assert_array_proximo(
        nominais(medidas_em_centimetros, "si"), np.array(valores_nominais) / 100
    )
    assert_array_proximo(
        nominais(medidas_em_centimetros, "m"), nominais(medidas_em_centimetros, "si")
    )


def test_nominais_rejeitam_valores_que_nao_sao_medidas() -> None:
    with pytest.raises(TypeError):
        nominais(np.arange(10), "")


@pytest.fixture
def valores_incerteza() -> list[float]:
    return [3.5, 4.003, 310, 0, 56]


@pytest.fixture
def medidas_com_incertezas(
    valores_incerteza: list[float], valores_nominais: list[float]
) -> list[Medida]:
    return [
        Medida(nominal, "cm", incerteza)
        for (nominal, incerteza) in zip(
            valores_nominais, valores_incerteza, strict=True
        )
    ]


def test_incertezas(
    medidas_com_incertezas: list[Medida], valores_incerteza: list[float]
) -> None:
    assert_array_proximo(
        incertezas(medidas_com_incertezas, "cm"), valores_incerteza, rtol=0
    )


def test_incertezas_convertem_para_si(
    medidas_com_incertezas: list[Medida],
) -> None:
    incertezas_em_centimetros = incertezas(medidas_com_incertezas, "cm")
    assert_array_proximo(
        incertezas(medidas_com_incertezas, "si"), incertezas_em_centimetros / 100
    )
    assert_array_proximo(
        incertezas(medidas_com_incertezas, "m"),
        incertezas(medidas_com_incertezas, "si"),
        rtol=0,
    )


def test_incertezas_rejeitam_valores_que_nao_sao_medidas() -> None:
    with pytest.raises(TypeError):
        incertezas(np.arange(10), "")


@pytest.fixture
def medidas_para_curva() -> list[Medida]:
    return [Medida(5, "", 0.1), Medida(9, "", 2), Medida(11, "", 0.5)]


@pytest.fixture
def amostragem_regressao() -> NDArray[np.object_]:
    x = np.array(
        [
            Medida(1, "cm", 0.1),
            Medida(2, "cm", 0.1),
            Medida(3, "cm", 0.1),
            Medida(4, "cm", 0.1),
            Medida(5, "cm", 0.1),
        ]
    )
    linha: AjustePolinomial = regressao_linear(x, x)
    return linha(x)


def test_curva_min(medidas_para_curva: list[Medida]) -> None:
    assert_array_proximo(curva_min(medidas_para_curva, ""), [4.8, 5, 10], rtol=0)
    assert_array_proximo(curva_min(medidas_para_curva, "", 3), [4.7, 3, 9.5], rtol=0)


def test_curva_max(medidas_para_curva: list[Medida]) -> None:
    assert_array_proximo(curva_max(medidas_para_curva, ""), [5.2, 13, 12], rtol=0)
    assert_array_proximo(curva_max(medidas_para_curva, "", 3), [5.3, 15, 12.5], rtol=0)


@pytest.mark.parametrize("calcular_curva", [curva_min, curva_max])
def test_curvas_rejeitam_valores_que_nao_sao_medidas(
    calcular_curva: Callable[[Iterable[Medida], str], NDArray[np.float64]],
) -> None:
    with pytest.raises(TypeError):
        calcular_curva(np.arange(10), "")


@pytest.mark.parametrize("sigmas", [0, -1])
def test_curvas_rejeitam_numero_de_sigmas_nao_positivo(
    amostragem_regressao: NDArray[np.object_], sigmas: int
) -> None:
    with pytest.raises(ValueError):
        curva_max(amostragem_regressao, "si", sigmas)
    with pytest.raises(ValueError):
        curva_min(amostragem_regressao, "si", sigmas)


def test_linspace() -> None:
    a = 1
    b = 20
    N = 20
    x = linspaceM(a, b, N, "", 0.1)
    assert np.all(nominais(x, "") == np.linspace(a, b, N))
    assert np.all(incertezas(x, "") == 0.1)


def test_converter_array() -> None:
    x = linspaceM(5, 10, 10, "mm", 0.01)
    esperado = np.linspace(0.5, 1, 10)  # cm
    assert_array_proximo(nominais(x, "cm"), esperado)


def test_converter_array_si() -> None:
    x = linspaceM(10, 50, 10, "cm", 0.01)
    esperado = np.linspace(0.1, 0.5, 10)  # si
    assert_array_proximo(nominais(x, "si"), esperado)


def test_array_m() -> None:
    x_dados = arrayM([1, 2, 3, 4, 5], "s", 0.01)
    for valor, esperado in zip(x_dados, range(1, 6), strict=True):
        assert_medida_proxima(valor, esperado, 0.01, "s", rtol=0)
    with pytest.raises(TypeError):
        arrayM(x_dados, "km/s", 0.01)
