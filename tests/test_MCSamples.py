import pytest

from LabIFSC2 import *


def test_operacoes_incompativeis():
    x=Medida(10,0.1,'m')
    x=x*x
    alterar_monte_carlo_samples(10_000)
    y=Medida(10,0.1,'m')
    y=y*y
    with pytest.raises(ValueError):
        x+y
    with pytest.raises(ValueError):
        alterar_monte_carlo_samples(0)
    with pytest.raises(ValueError):
        alterar_monte_carlo_samples(-3)
def test_especionando_histograma():
    alterar_monte_carlo_samples(100_000)
    x=Medida(10,0.1,'m')
    assert len(x.histograma)==100_000
    alterar_monte_carlo_samples(10_000)
    y=Medida(10,0.1,'m')
    assert len(y.histograma)==10_000
    alterar_monte_carlo_samples(100_000)
