import numpy as np
from numpy.typing import ArrayLike

from LabIFSC2 import Medida

TOLERANCIA_MONTE_CARLO = 1e-4
# "random" number smashed outta my keyboard
SEMENTE_MONTE_CARLO = 13765130613613057380967138671308671380961


def assert_medida_proxima(
    medida: Medida,
    nominal: float,
    incerteza: float,
    unidade: str = "",
    *,
    rtol: float = TOLERANCIA_MONTE_CARLO,
    atol: float = 0,
) -> None:
    np.testing.assert_allclose(medida.nominal(unidade), nominal, rtol=rtol, atol=atol)
    np.testing.assert_allclose(
        medida.incerteza(unidade), incerteza, rtol=rtol, atol=atol
    )


def assert_array_proximo(
    obtido: ArrayLike,
    esperado: ArrayLike,
    *,
    rtol: float = TOLERANCIA_MONTE_CARLO,
    atol: float = 0,
) -> None:
    array_obtido = np.asarray(obtido, dtype=np.float64)
    array_esperado = np.asarray(esperado, dtype=np.float64)
    np.testing.assert_allclose(array_obtido, array_esperado, rtol=rtol, atol=atol)
