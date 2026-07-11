from typing import cast

import numpy as np
import pytest
from numpy.typing import NDArray
from scipy.optimize import curve_fit  # type: ignore[import-untyped]

import LabIFSC2 as lab
from tests.utilities import assert_array_proximo, assert_medida_proxima


def modelo_exponencial(
    x: NDArray[np.float64], amplitude: float, expoente: float
) -> NDArray[np.float64]:
    return amplitude * np.exp(expoente * x)


@pytest.fixture
def ajuste_exponencial() -> lab.AjusteExponencial:
    return lab.AjusteExponencial(
        amplitude=lab.Medida(1, "", 0.1), expoente=lab.Medida(3, "", 0.01)
    )


def test_ajuste_exponencial_armazena_parametros(
    ajuste_exponencial: lab.AjusteExponencial,
) -> None:
    assert_medida_proxima(ajuste_exponencial.amplitude, 1, 0.1, rtol=0)
    assert_medida_proxima(ajuste_exponencial.expoente, 3, 0.01, rtol=0)
    assert tuple(ajuste_exponencial) == (
        ajuste_exponencial.amplitude,
        ajuste_exponencial.expoente,
    )
    assert (
        str(ajuste_exponencial)
        == "AjusteExponencial(amplitude=(1,0 ± 0,1) , expoente=(3,00 ± 0,01) )"
    )


def test_regressao_exponencial_rejeita_y_nao_positivo() -> None:
    x = lab.linspaceM(3, 1, 10, "", 0.1)
    y = lab.linspaceM(-3, 1, 10, "", 0.1)
    with pytest.raises(ValueError, match="positivos"):
        lab.regressao_exponencial(x, y)


def test_regressao_exponencial_rejeita_base_menor_que_um() -> None:
    x = lab.linspaceM(1, 3, 10, "", 0.1)
    with pytest.raises(ValueError, match="Base"):
        lab.regressao_exponencial(x, x, base=0.8)


def test_ajuste_exponencial_avalia_array(
    ajuste_exponencial: lab.AjusteExponencial,
) -> None:
    x = lab.linspaceM(0, 1, 10, "", 0)
    valores = cast(NDArray[np.object_], ajuste_exponencial(x))
    assert_array_proximo(
        lab.nominais(valores, ""),
        modelo_exponencial(
            np.linspace(0, 1, 10),
            ajuste_exponencial.amplitude.nominal(""),
            ajuste_exponencial.expoente.nominal(""),
        ),
        rtol=5e-4,
    )


@pytest.mark.parametrize(
    ("amplitude", "expoente"),
    [(3.6, 1.05), (2.0, 0.5), (1.0, -2.0), (4.5, -0.75), (3.0, 1.5), (1, 0)],
)
def test_regressao_exponencial_equivale_ao_scipy(
    amplitude: float,
    expoente: float,
    rng_testes: np.random.Generator,
) -> None:
    ruido = rng_testes.normal(1, 0.001, 100)
    x_numerico = np.linspace(3, 10, 100)
    y_numerico = modelo_exponencial(x_numerico, amplitude, expoente) * ruido
    parametros_scipy, _ = curve_fit(
        modelo_exponencial, x_numerico, y_numerico, p0=[amplitude, expoente]
    )

    x = lab.linspaceM(3, 10, 100, "", 0.01)
    y = modelo_exponencial(x_numerico, amplitude, expoente) * ruido
    ajuste = lab.regressao_exponencial(x, lab.arrayM(y, "", 0.01))

    np.testing.assert_allclose(
        ajuste.amplitude.nominal(""), parametros_scipy[0], rtol=1e-3, atol=1e-3
    )
    np.testing.assert_allclose(
        ajuste.expoente.nominal(""), parametros_scipy[1], rtol=1e-3, atol=1e-3
    )
