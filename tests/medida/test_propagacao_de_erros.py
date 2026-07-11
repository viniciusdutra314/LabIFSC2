from collections.abc import Callable

import mcerp  # type: ignore[import-untyped]
import mcerp.umath as umath  # type: ignore[import-untyped]
import numpy as np
import pytest
from mcerp.core import UncertainFunction  # type: ignore[import-untyped]

import LabIFSC2 as lab
from tests.medida.utilities import assert_propagacao_igual_mcerp

OperacaoLab = Callable[[lab.Medida], lab.Medida]
OperacaoMcerp = Callable[[UncertainFunction], UncertainFunction]


@pytest.mark.parametrize(
    ("operacao_lab", "operacao_mcerp"),
    [
        (lambda x: x + lab.Medida(2, "", 0.03), lambda x: x + mcerp.N(2, 0.03)),
        (lambda x: x - lab.Medida(2, "", 0.03), lambda x: x - mcerp.N(2, 0.03)),
        (lambda x: x * lab.Medida(2, "", 0.03), lambda x: x * mcerp.N(2, 0.03)),
        (lambda x: x / lab.Medida(2, "", 0.03), lambda x: x / mcerp.N(2, 0.03)),
        (lambda x: x ** lab.Medida(2, "", 0.03), lambda x: x ** mcerp.N(2, 0.03)),
    ],
)
def test_operacoes_entre_medidas_conferem_com_mcerp(
    operacao_lab: OperacaoLab,
    operacao_mcerp: OperacaoMcerp,
) -> None:
    obtido = operacao_lab(lab.Medida(5, "", 0.02))
    esperado = operacao_mcerp(mcerp.N(5, 0.02))
    assert_propagacao_igual_mcerp(obtido, esperado)


@pytest.mark.parametrize(
    ("operacao_lab", "operacao_mcerp"),
    [
        (lambda x: x * 3, lambda x: x * 3),
        (lambda x: x / 15, lambda x: x / 15),
        (lambda x: -53 / x, lambda x: -53 / x),
        (lambda x: x**3, lambda x: x**3),
        (lambda x: 3**x, lambda x: 3**x),
        (lambda x: -x, lambda x: -x),
        (lambda x: abs(x), lambda x: abs(x)),
        (lambda x: +x, lambda x: +x),
    ],
)
def test_operacoes_com_escalares_conferem_com_mcerp(
    operacao_lab: OperacaoLab,
    operacao_mcerp: OperacaoMcerp,
) -> None:
    obtido = operacao_lab(lab.Medida(2, "", 0.01))
    esperado = operacao_mcerp(mcerp.N(2, 0.01))
    assert_propagacao_igual_mcerp(obtido, esperado)


@pytest.mark.parametrize(
    ("funcao_lab", "funcao_mcerp", "valor"),
    [
        (np.sin, umath.sin, 0.4),
        (np.cos, umath.cos, 0.4),
        (np.tan, umath.tan, 0.4),
        (np.arcsin, umath.asin, 0.4),
        (np.arccos, umath.acos, 0.4),
        (np.arctan, umath.atan, 0.4),
        (np.sinh, umath.sinh, 0.4),
        (np.cosh, umath.cosh, 0.4),
        (np.tanh, umath.tanh, 0.4),
        (np.arcsinh, umath.asinh, 1.4),
        (np.arccosh, umath.acosh, 1.4),
        (np.arctanh, umath.atanh, 0.4),
        (np.exp, umath.exp, 1.4),
        (np.sqrt, umath.sqrt, 1.4),
        (np.cbrt, lambda x: x ** (1 / 3), 1.4),
        (np.log, umath.log, 1.4),
        (np.log2, lambda x: umath.log(x) / np.log(2), 1.4),
        (np.log10, umath.log10, 1.4),
    ],
)
def test_funcoes_numpy_conferem_com_mcerp(
    funcao_lab: OperacaoLab,
    funcao_mcerp: OperacaoMcerp,
    valor: float,
) -> None:
    obtido = funcao_lab(lab.Medida(valor, "", 1e-3))
    esperado = funcao_mcerp(mcerp.N(valor, 1e-3))
    assert_propagacao_igual_mcerp(obtido, esperado)


def test_correlacao_preserva_a_mesma_amostra() -> None:
    medida = lab.Medida(2, "", 0.1)
    quadrado = medida * medida
    esperado = mcerp.N(2, 0.1) ** 2
    assert_propagacao_igual_mcerp(quadrado, esperado)
    referencia = mcerp.N(2, 0.1)
    assert_propagacao_igual_mcerp(medida / medida, referencia / referencia)


@pytest.mark.parametrize(
    ("ufunc", "operacao"),
    [
        (np.add, lambda x, y: x + y),
        (np.subtract, lambda x, y: x - y),
        (np.multiply, lambda x, y: x * y),
        (np.divide, lambda x, y: x / y),
        (np.power, lambda x, y: x**y),
    ],
)
def test_ufuncs_aritmeticas_usam_as_operacoes_de_medida(
    ufunc: Callable[[lab.Medida, lab.Medida], lab.Medida],
    operacao: Callable[[lab.Medida, lab.Medida], lab.Medida],
) -> None:
    esquerda = lab.Medida(2, "", 0.01)
    direita = lab.Medida(3, "", 0.01)

    obtido = ufunc(esquerda, direita)
    esperado = operacao(esquerda, direita)

    np.testing.assert_allclose(obtido.nominal(""), esperado.nominal(""))
    np.testing.assert_allclose(obtido.incerteza(""), esperado.incerteza(""), rtol=5e-3)
