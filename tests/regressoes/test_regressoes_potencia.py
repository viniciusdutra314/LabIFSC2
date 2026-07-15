import sys
from typing import assert_type

import numpy as np
import pytest
from numpy.typing import NDArray

import LabIFSC2 as lab


def modelo_potencia(
    x: NDArray[np.float64], amplitude: float, potencia: float
) -> NDArray[np.float64]:
    return amplitude * np.power(x, potencia)


@pytest.mark.skipif(
    sys.implementation.name == "pypy",
    reason="SciPy não está disponível no PyPy",
)
@pytest.mark.parametrize(
    ("amplitude", "potencia"),
    [(3.6, 1.05), (2.0, 0.5), (1.0, -2.0), (4.5, -0.75), (3.0, 1.5), (1, 0.05)],
)
def test_regressao_potencia_equivale_ao_scipy(
    amplitude: float,
    potencia: float,
    rng_testes: np.random.Generator,
) -> None:
    from scipy.optimize import curve_fit  # type: ignore[import-untyped]

    ruido = rng_testes.normal(1, 0.002, 100)
    x_numerico = np.linspace(3, 10, 100)
    y_numerico = modelo_potencia(x_numerico, amplitude, potencia) * ruido
    parametros_scipy, _ = curve_fit(modelo_potencia, x_numerico, y_numerico)

    x = lab.linspaceM(3, 10, 100, "", 0.01)
    y = lab.arrayM(y_numerico, "", 0.01)
    ajuste = lab.regressao_potencia(x, y)

    np.testing.assert_allclose(
        ajuste.amplitude.nominal(""), parametros_scipy[0], rtol=1e-3, atol=1e-3
    )
    np.testing.assert_allclose(
        ajuste.potencia.nominal(""), parametros_scipy[1], rtol=1e-3, atol=1e-3
    )


@pytest.mark.parametrize(
    ("x_fixture", "y_fixture"),
    [
        ("medidas_nao_positivas", "medidas_positivas"),
        ("medidas_positivas", "medidas_nao_positivas"),
        ("medidas_nao_positivas", "medidas_nao_positivas"),
    ],
)
def test_regressao_potencia_rejeita_valores_nao_positivos(
    x_fixture: str, y_fixture: str, request: pytest.FixtureRequest
) -> None:
    x: NDArray[np.object_] = request.getfixturevalue(x_fixture)
    y: NDArray[np.object_] = request.getfixturevalue(y_fixture)
    with pytest.raises(ValueError, match="positivos"):
        lab.regressao_potencia(x, y)


def test_regressao_potencia_aceita_x0() -> None:
    amplitude = 3.0
    potencia = 2.0
    x = lab.linspaceM(1, 10, 100, "m", 0.01)
    x0 = lab.Medida(2.0, "m")
    y = amplitude * (x / x0) ** potencia

    ajuste = lab.regressao_potencia(x, y, x0=x0)

    np.testing.assert_allclose(ajuste.amplitude.nominal(""), amplitude, rtol=1e-2)
    np.testing.assert_allclose(ajuste.potencia.nominal(""), potencia, rtol=1e-2)
    np.testing.assert_allclose(ajuste.x0.nominal("m"), 2.0, rtol=1e-5)
    valor = assert_type(ajuste(x0), lab.Medida)
    assert_type(ajuste(x), NDArray[np.object_])
    np.testing.assert_allclose(valor.nominal(""), amplitude, rtol=1e-3)
    assert (
        str(ajuste) == "AjusteLeiDePotencia(amplitude=(3,000095 ± 0,000005), "
        "potencia=(1,999975 ± 0,000002), x0=2 m)"
    )
