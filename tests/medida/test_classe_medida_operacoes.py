from collections.abc import Callable
from typing import cast

import numpy as np
import pytest
from numpy.typing import NDArray
from pint import Quantity

import LabIFSC2 as lab
from tests.utilities import assert_medida_proxima


def test_operacoes_com_a_mesma_medida_preservam_correlacao() -> None:
    medida = lab.Medida(5, "", 0.1)
    medida_clone = lab.Medida(5, "", 0.1)
    assert_medida_proxima(medida + medida, 10, 0.2)
    assert_medida_proxima(medida - medida, 0, 0)
    assert_medida_proxima(medida / medida, 1, 0)
    with pytest.raises(AssertionError):
        assert_medida_proxima(medida + medida_clone, 10, 0.2)
    with pytest.raises(AssertionError):
        assert_medida_proxima(medida - medida_clone, 0, 0.0)
    with pytest.raises(AssertionError):
        assert_medida_proxima(medida / medida_clone, 1, 0)


@pytest.mark.parametrize(
    ("operacao", "transformacao_no_histograma"),
    [
        (lambda medida: medida + 3, lambda amostras: amostras + 3),
        (lambda medida: 3 + medida, lambda amostras: 3 + amostras),
        (lambda medida: medida - 3, lambda amostras: amostras - 3),
        (lambda medida: 3 - medida, lambda amostras: 3 - amostras),
        (lambda medida: medida * -3, lambda histograma: histograma * -3),
        (lambda medida: medida / -3, lambda histograma: histograma / -3),
        (lambda medida: -medida, lambda histograma: -histograma),
        (lambda medida: abs(medida), lambda histograma: abs(histograma)),
        (lambda medida: +medida, lambda histograma: histograma),
    ],
)
def test_operacoes_exatas_transformam_cada_amostra_do_histograma(
    operacao: Callable[[lab.Medida], lab.Medida],
    transformacao_no_histograma: Callable[[NDArray[np.float64]], NDArray[np.float64]],
) -> None:
    medida = lab.Medida(-5, "m", 0.1)
    histograma_original = medida.histograma
    assert isinstance(histograma_original, Quantity)

    histograma_resultado = operacao(medida).histograma
    assert isinstance(histograma_resultado, Quantity)
    np.testing.assert_allclose(
        histograma_resultado.magnitude,
        transformacao_no_histograma(
            cast(NDArray[np.float64], histograma_original.magnitude)
        ),
    )


@pytest.mark.parametrize(
    "operacao",
    [
        lambda medida: "3" / medida,
        lambda medida: medida ** "3",
        lambda medida: "3" ** medida,
        lambda medida: medida // 2,
        lambda medida: medida % 2,
        lambda medida: divmod(medida, 2),
    ],
)
def test_operacoes_nao_suportadas_levantam_type_error(
    operacao: Callable[[lab.Medida], object],
) -> None:
    with pytest.raises(TypeError):
        operacao(lab.Medida(6, "", 0.1))


OperacaoVetorizada = Callable[[lab.Medida, NDArray[np.object_]], NDArray[np.object_]]
OperacaoEscalar = Callable[[lab.Medida, lab.Medida], lab.Medida]


@pytest.mark.parametrize(
    ("operacao_vetorizada", "operacao_elemento"),
    [
        (lambda escalar, array: escalar + array, lambda escalar, item: escalar + item),
        (lambda escalar, array: array + escalar, lambda escalar, item: item + escalar),
        (lambda escalar, array: escalar - array, lambda escalar, item: escalar - item),
        (lambda escalar, array: array - escalar, lambda escalar, item: item - escalar),
        (lambda escalar, array: escalar * array, lambda escalar, item: escalar * item),
        (lambda escalar, array: array * escalar, lambda escalar, item: item * escalar),
        (lambda escalar, array: escalar / array, lambda escalar, item: escalar / item),
        (lambda escalar, array: array / escalar, lambda escalar, item: item / escalar),
        (lambda escalar, array: escalar**array, lambda escalar, item: escalar**item),
        (lambda escalar, array: array**escalar, lambda escalar, item: item**escalar),
    ],
)
def test_operacoes_entre_medida_e_array_sao_elemento_a_elemento(
    operacao_vetorizada: OperacaoVetorizada,
    operacao_elemento: OperacaoEscalar,
) -> None:
    escalar = lab.Medida(2, "", 0.01)
    medidas = lab.arrayM([1, 2, 4], "", 0.02)

    resultado = operacao_vetorizada(escalar, medidas)

    assert isinstance(resultado, np.ndarray)
    assert resultado.shape == medidas.shape
    assert resultado.dtype == object
    for obtido, item in zip(resultado, medidas, strict=True):
        assert isinstance(obtido, lab.Medida)
        esperado = operacao_elemento(escalar, item)
        assert_medida_proxima(
            obtido,
            esperado.nominal(""),
            esperado.incerteza(""),
            rtol=1e-3,
            atol=1e-6,
        )


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
