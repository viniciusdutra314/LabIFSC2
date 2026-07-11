from collections.abc import Iterator

import mcerp
import numpy as np
import pytest
from numpy.typing import NDArray

import LabIFSC2 as lab
from tests.utilities import SEMENTE_MONTE_CARLO


@pytest.fixture(autouse=True)
def configurar_rng_mcerp() -> Iterator[None]:
    estado = np.random.get_state()
    quantidade_amostras = mcerp.npts
    np.random.seed(SEMENTE_MONTE_CARLO % 2**32)
    mcerp.npts = 100_000
    try:
        yield
    finally:
        np.random.set_state(estado)
        mcerp.npts = quantidade_amostras


@pytest.fixture
def rng_testes() -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(SEMENTE_MONTE_CARLO))


@pytest.fixture
def medida() -> lab.Medida:
    return lab.Medida(5, "m", 0.1)


@pytest.fixture
def medida_adimensional() -> lab.Medida:
    return lab.Medida(2, "", 0.01)


@pytest.fixture
def medidas_ordenadas() -> NDArray[np.object_]:
    return lab.linspaceM(0, 10, 11, "s", 0.1)


@pytest.fixture
def medidas_desordenadas() -> NDArray[np.object_]:
    return lab.arrayM([4, 1, 3, 2, 7, 5, 9, 6, 8, 10], "s", 0)


@pytest.fixture
def amostras_monte_carlo_reduzidas() -> Iterator[None]:
    lab.alterar_monte_carlo_samples(10_000)
    try:
        yield
    finally:
        lab.alterar_monte_carlo_samples(100_000)
