from typing import cast

import numpy as np
import pytest
from numpy.typing import NDArray

import LabIFSC2 as lab
from tests.utilities import assert_array_proximo


def teste_ajuste_polinomial() -> None:
    polinomio = lab.AjustePolinomial(lab.arrayM([1, 2, 3, 4], "", 0))
    assert polinomio.grau == 3
    assert [coef.nominal("") for coef in polinomio.coef] == [1, 2, 3, 4]
    a, b, c, d = polinomio
    assert a.nominal("") == 4
    assert b.nominal("") == 3
    assert c.nominal("") == 2
    assert d.nominal("") == 1
    with pytest.raises(TypeError):
        polinomio(0)  # type: ignore[arg-type]
    avaliado=cast(lab.Medida,polinomio(lab.Medida(0, "", 0)))
    assert avaliado.nominal("") == d.nominal("")


@pytest.fixture
def dados_quadraticos() -> tuple[NDArray[np.object_], NDArray[np.object_]]:
    x = lab.arrayM([1, 2, 3, 4, 5], "", 0.1)
    y = lab.arrayM([1, 4, 9, 16, 25], "", 0.1)
    return x, y


@pytest.fixture
def ajuste_quadratico(
    dados_quadraticos: tuple[NDArray[np.object_], NDArray[np.object_]],
) -> lab.AjustePolinomial:
    x, y = dados_quadraticos
    return lab.regressao_polinomial(x, y, 2)


def test_regressao_linear_equivale_ao_numpy(
    rng_testes: np.random.Generator,
) -> None:
    x_numerico = np.arange(10, dtype=float)
    y_numerico = 2.5 * x_numerico - 1.2 + rng_testes.normal(0, 0.01, 10)
    coeficientes_numpy, covariancia = np.polyfit(x_numerico, y_numerico, 1, cov=True)
    incertezas_numpy = np.sqrt(np.diag(covariancia))

    ajuste = lab.regressao_linear(
        lab.arrayM(x_numerico, "s", 0.01), lab.arrayM(y_numerico, "m", 0.01)
    )
    a,b = ajuste

    np.testing.assert_allclose(
        a.nominal("m/s"), coeficientes_numpy[0], rtol=1e-3
    )
    np.testing.assert_allclose(
        b.nominal("m"), coeficientes_numpy[1], rtol=1e-3
    )
    np.testing.assert_allclose(
        a.incerteza("m/s"), incertezas_numpy[0], rtol=1e-3
    )
    np.testing.assert_allclose(
        b.incerteza("m"), incertezas_numpy[1], rtol=1e-3
    )


def test_regressao_quadratica_recupera_reta(
    rng_testes: np.random.Generator,
) -> None:
    x_numerico = np.arange(100, dtype=float)
    y_numerico = 2.5 * x_numerico - 1.2 + rng_testes.normal(0, 0.001, 100)
    ajuste = lab.regressao_polinomial(
        lab.arrayM(x_numerico, "s", 0.01), lab.arrayM(y_numerico, "m", 0.01), 2
    )
    c, b, a = ajuste.coef

    np.testing.assert_allclose(a.nominal("m/s²"), 0, atol=1e-2)
    np.testing.assert_allclose(b.nominal("m/s"), 2.5, rtol=1e-1)
    np.testing.assert_allclose(c.nominal("m"), -1.2, rtol=1e-1)


def test_ajuste_polinomial_avalia_array() -> None:
    coeficientes = [
        lab.Medida(4, "", 0.001),
        lab.Medida(3, "", 0.001),
        lab.Medida(2, "", 0.001),
    ]
    ajuste = lab.AjustePolinomial(coeficientes)
    x = lab.arrayM([1, 2, 3], "", 0.1)
    resultado = cast(NDArray[np.object_], ajuste(x))

    assert_array_proximo(lab.nominais(resultado, ""), [9, 18, 31], rtol=5e-3)


def test_regressao_polinomial_rejeita_tamanhos_diferentes() -> None:
    x = lab.arrayM([1, 2, 3], "", 0)
    y = lab.arrayM([1, 4, 9, 16], "", 0)
    with pytest.raises(ValueError, match="não tem o mesmo tamanho"):
        lab.regressao_polinomial(x, y, 2)


def test_regressao_polinomial_rejeita_dados_insuficientes() -> None:
    x = lab.arrayM([1, 2], "", 0)
    y = lab.arrayM([1, 4], "", 0)
    with pytest.raises(ValueError, match="dados suficientes"):
        lab.regressao_polinomial(x, y, 1)


def test_regressao_polinomial_rejeita_valores_que_nao_sao_medidas() -> None:
    x = np.array([1, 2, 3, 4])
    y = np.array([1, 4, 7, 6])
    with pytest.raises(TypeError, match="Medida"):
        lab.regressao_polinomial(x, y, 1)
