import numpy as np
import pytest
from numpy.typing import NDArray

from LabIFSC2 import arrayM, linspaceM
from tests.utilities import SEMENTE_MONTE_CARLO


@pytest.fixture
def rng_testes() -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(SEMENTE_MONTE_CARLO))


@pytest.fixture
def campo_magnetico() -> NDArray[np.object_]:
    return arrayM([210, 90, 70, 54, 39, 32, 33, 27, 22, 20], "muT", 1)


@pytest.fixture
def distancias() -> NDArray[np.object_]:
    return linspaceM(1, 10, 10, "cm", 0.01)


@pytest.fixture
def medidas_unidade_incompativel() -> NDArray[np.object_]:
    return linspaceM(1, 10, 10, "kg", 0.001)


@pytest.fixture
def medidas_positivas() -> NDArray[np.object_]:
    return linspaceM(5, 10, 11, "", 0.01)


@pytest.fixture
def medidas_nao_positivas() -> NDArray[np.object_]:
    return linspaceM(-5, 5, 11, "", 0.01)
