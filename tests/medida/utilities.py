from typing import Protocol

import numpy as np

from LabIFSC2 import Medida


class ResultadoMcerp(Protocol):
    @property
    def mean(self) -> float: ...

    @property
    def std(self) -> float: ...


def assert_propagacao_igual_mcerp(
    medida: Medida,
    esperado: ResultadoMcerp,
    unidade: str = "",
    *,
    rtol_nominal: float = 1e-3,
    rtol_incerteza: float = 5e-3,
    atol: float = 1e-7,
) -> None:
    np.testing.assert_allclose(
        medida.nominal(unidade), esperado.mean, rtol=rtol_nominal, atol=atol
    )
    np.testing.assert_allclose(
        medida.incerteza(unidade), esperado.std, rtol=rtol_incerteza, atol=atol
    )
