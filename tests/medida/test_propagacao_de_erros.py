from collections.abc import Callable

import numpy as np
import pytest

import LabIFSC2 as lab
from tests.utilities import assert_medida_proxima


@pytest.mark.parametrize(
    ("operacao", "nominal", "incerteza"),
    [
        (lambda x, y: x + y, 7.0, np.hypot(0.02, 0.03)),
        (lambda x, y: x - y, 3.0, np.hypot(0.02, 0.03)),
        (lambda x, y: x * y, 10.0, np.hypot(2 * 0.02, 5 * 0.03)),
        (lambda x, y: x / y, 2.5, np.hypot(0.02 / 2, 5 * 0.03 / 4)),
    ],
)
def test_propagacao_operacoes_binarias(
    operacao: Callable[[lab.Medida, lab.Medida], lab.Medida],
    nominal: float,
    incerteza: float,
) -> None:
    resultado = operacao(lab.Medida(5, "", 0.02), lab.Medida(2, "", 0.03))
    assert_medida_proxima(resultado, nominal, incerteza, rtol=8e-3, atol=1e-4)


@pytest.mark.parametrize(
    ("funcao", "valor", "esperado", "derivada"),
    [
        (np.sin, 0.4, np.sin(0.4), np.cos(0.4)),
        (np.cos, 0.4, np.cos(0.4), -np.sin(0.4)),
        (np.tan, 0.4, np.tan(0.4), 1 / np.cos(0.4) ** 2),
        (np.arcsin, 0.4, np.arcsin(0.4), 1 / np.sqrt(1 - 0.4**2)),
        (np.arccos, 0.4, np.arccos(0.4), -1 / np.sqrt(1 - 0.4**2)),
        (np.arctan, 0.4, np.arctan(0.4), 1 / (1 + 0.4**2)),
        (np.sinh, 0.4, np.sinh(0.4), np.cosh(0.4)),
        (np.cosh, 0.4, np.cosh(0.4), np.sinh(0.4)),
        (np.tanh, 0.4, np.tanh(0.4), 1 / np.cosh(0.4) ** 2),
        (np.arcsinh, 1.4, np.arcsinh(1.4), 1 / np.sqrt(1 + 1.4**2)),
        (np.arccosh, 1.4, np.arccosh(1.4), 1 / np.sqrt(1.4**2 - 1)),
        (np.arctanh, 0.4, np.arctanh(0.4), 1 / (1 - 0.4**2)),
        (np.exp, 1.4, np.exp(1.4), np.exp(1.4)),
        (np.sqrt, 1.4, np.sqrt(1.4), 1 / (2 * np.sqrt(1.4))),
        (np.cbrt, 1.4, np.cbrt(1.4), 1 / (3 * np.cbrt(1.4) ** 2)),
        (np.log, 1.4, np.log(1.4), 1 / 1.4),
        (np.log2, 1.4, np.log2(1.4), 1 / (1.4 * np.log(2))),
        (np.log10, 1.4, np.log10(1.4), 1 / (1.4 * np.log(10))),
    ],
)
def test_funcoes_numpy_propagam_incerteza(
    funcao: Callable[[lab.Medida], lab.Medida],
    valor: float,
    esperado: float,
    derivada: float,
) -> None:
    incerteza = 1e-4
    resultado = funcao(lab.Medida(valor, "", incerteza))
    assert_medida_proxima(
        resultado, esperado, abs(derivada) * incerteza, rtol=8e-3, atol=1e-7
    )


@pytest.mark.parametrize(
    ("operacao", "nominal", "derivada"),
    [
        (lambda x: x**3, 8.0, 12.0),
        (lambda x: np.power(x, 3), 8.0, 12.0),
        (lambda x: 3**x, 9.0, 9 * np.log(3)),
    ],
)
def test_potencias_propagam_incerteza(
    operacao: Callable[[lab.Medida], lab.Medida],
    nominal: float,
    derivada: float,
) -> None:
    resultado = operacao(lab.Medida(2, "", 1e-4))
    assert_medida_proxima(resultado, nominal, derivada * 1e-4, rtol=8e-3, atol=1e-6)


def test_funcao_numpy_nao_suportada_levanta_erro(
    medida_adimensional: lab.Medida,
) -> None:
    with pytest.raises(TypeError):
        np.floor(medida_adimensional)  # type: ignore[call-overload]


def test_atributo_inexistente_levanta_erro(medida_adimensional: lab.Medida) -> None:
    with pytest.raises(AttributeError):
        medida_adimensional.funcao_inexistente()
