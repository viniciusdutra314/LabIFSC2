from collections.abc import Callable
from typing import Protocol, cast

import numpy as np
import pytest
from numpy.core.numerictypes import object_
from numpy.typing import NDArray
from pint.errors import DimensionalityError

from LabIFSC2 import (
    Medida,
    nominais,
    regressao_exponencial,
    regressao_linear,
    regressao_polinomial,
    regressao_potencia,
)


class Ajuste(Protocol):
    def __call__(
        self, medidas: NDArray[np.object_]
    ) -> Medida | NDArray[np.object_]: ...


def assert_ajuste_preserva_unidade(
    ajuste: Ajuste,
    distancias: NDArray[np.object_],
    campo_magnetico: NDArray[np.object_],
) -> None:
    valores = nominais(cast(NDArray[object_], ajuste(distancias)), "muT")
    assert valores.shape == campo_magnetico.shape


@pytest.mark.parametrize("grau", range(1, 7))
def test_regressao_polinomial_preserva_unidades(
    distancias: NDArray[np.object_],
    campo_magnetico: NDArray[np.object_],
    grau: int,
) -> None:
    assert_ajuste_preserva_unidade(
        regressao_polinomial(distancias, campo_magnetico, grau),
        distancias,
        campo_magnetico,
    )


@pytest.mark.parametrize("regressao", [regressao_exponencial, regressao_potencia])
def test_regressoes_nao_lineares_preservam_unidades(
    regressao: Callable[[NDArray[np.object_], NDArray[np.object_]], Ajuste],
    distancias: NDArray[np.object_],
    campo_magnetico: NDArray[np.object_],
) -> None:
    assert_ajuste_preserva_unidade(
        regressao(distancias, campo_magnetico), distancias, campo_magnetico
    )


@pytest.mark.parametrize(
    "regressao",
    [regressao_linear, regressao_exponencial, regressao_potencia],
)
def test_regressoes_rejeitam_unidade_de_entrada_incompativel(
    regressao: Callable[[NDArray[np.object_], NDArray[np.object_]], Ajuste],
    distancias: NDArray[np.object_],
    campo_magnetico: NDArray[np.object_],
    medidas_unidade_incompativel: NDArray[np.object_],
) -> None:
    ajuste = regressao(distancias, campo_magnetico)
    with pytest.raises((DimensionalityError, ValueError)):
        nominais(cast(NDArray[np.object_], ajuste(medidas_unidade_incompativel)), "muT")


def test_regressao_rejeita_unidade_de_saida_incompativel(
    distancias: NDArray[np.object_], campo_magnetico: NDArray[np.object_]
) -> None:
    ajuste = regressao_linear(distancias, campo_magnetico)
    with pytest.raises(DimensionalityError):
        nominais(cast(NDArray[np.object_], ajuste(distancias)), "kg")
