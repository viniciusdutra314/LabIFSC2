from collections.abc import Iterator

import numpy as np
import pytest

from LabIFSC2 import alterar_monte_carlo_rng
from tests.utilities import SEMENTE_MONTE_CARLO


@pytest.fixture(autouse=True)
def configurar_rng_monte_carlo() -> Iterator[None]:
    gerador = np.random.Generator(np.random.PCG64(SEMENTE_MONTE_CARLO))
    alterar_monte_carlo_rng(gerador)
    yield
