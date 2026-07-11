import numpy as np
import pytest
from numpy.typing import NDArray
from pint import Quantity

import LabIFSC2 as lab


def test_alterar_monte_carlo_rng() -> None:
    lab.alterar_monte_carlo_rng(np.random.default_rng(42))
    primeiro_histograma = lab.Medida(5, "m", 0.1).histograma
    lab.alterar_monte_carlo_rng(np.random.default_rng(42))
    segundo_histograma = lab.Medida(5, "m", 0.1).histograma
    assert isinstance(primeiro_histograma, Quantity)
    assert isinstance(segundo_histograma, Quantity)
    assert primeiro_histograma.units == segundo_histograma.units
    np.testing.assert_array_equal(
        primeiro_histograma.magnitude, segundo_histograma.magnitude
    )


def test_alterar_monte_carlo_rng_tipo_invalido() -> None:
    with pytest.raises(TypeError, match="numpy.random.Generator"):
        lab.alterar_monte_carlo_rng(42)  # type: ignore[arg-type]


@pytest.mark.parametrize("quantidade", [0, -1])
def test_alterar_monte_carlo_samples_rejeita_valor_nao_positivo(
    quantidade: int,
) -> None:
    with pytest.raises(ValueError, match="maior que 0"):
        lab.alterar_monte_carlo_samples(quantidade)


@pytest.mark.parametrize("incerteza", [-1, -0.01])
def test_inicializacao_rejeita_incerteza_negativa(incerteza: float) -> None:
    with pytest.raises(ValueError, match="Incerteza não pode ser negativa"):
        lab.Medida(5, "", incerteza)


def test_inicializacao_escalar_e_conversao_si(medida: lab.Medida) -> None:
    assert medida.nominal("si") == pytest.approx(5)
    assert medida.incerteza("SI") == pytest.approx(0.1)
    assert medida.nominal("cm") == pytest.approx(500)
    assert medida.incerteza("cm") == pytest.approx(10)
    assert medida.dimensao == lab.Medida(1, "km").dimensao


def test_inicializacao_por_amostras_usa_media_e_desvio_amostral() -> None:
    medida = lab.Medida([1, 2, 3], "s")
    assert medida.nominal("s") == pytest.approx(2)
    assert medida.incerteza("s") == pytest.approx(np.std([1, 2, 3], ddof=1))
    assert medida.incerteza("s") != pytest.approx(np.std([1, 2, 3]))  # without ddof=1


def test_inicializacao_por_amostras_preserva_maior_incerteza() -> None:
    medida = lab.Medida((1, 2, 3), "s", 2)
    assert medida.incerteza("s") == pytest.approx(2)


@pytest.mark.parametrize("amostras", [[], [1]])
def test_inicializacao_rejeita_amostras_insuficientes(amostras: list[float]) -> None:
    with pytest.raises(ValueError, match="pelo menos 2"):
        lab.Medida(amostras, "m")


def test_histograma_exato() -> None:
    medida = lab.Medida(5, "m")
    histograma = medida.histograma
    assert isinstance(histograma, Quantity)
    assert histograma.magnitude == 5


def test_gt_ge_lt_le():
    x = lab.Medida(5, "m", 0.1)
    y = lab.Medida(5, "m", 0.1)
    assert not (x > y)
    assert x >= y
    assert x <= y
    assert not (x > x)
    assert not (x < x)
    assert x >= x
    assert x <= x

    z = lab.Medida(6, "m", 0.1)
    assert z > x
    assert not (x > z)
    assert x < z
    assert x <= z
    assert not (x >= z)


def test_min_max_python(medidas_ordenadas: NDArray[np.object_]) -> None:
    tempos = medidas_ordenadas
    assert max(tempos) is tempos[-1]
    assert min(tempos) is tempos[0]


def test_min_max_numpy(medidas_ordenadas: NDArray[np.object_]) -> None:
    tempos = medidas_ordenadas
    assert np.max(tempos) is tempos[-1]
    assert np.min(tempos) is tempos[0]


def test_sorted_numpy(medidas_desordenadas: NDArray[np.object_]) -> None:
    tempos = medidas_desordenadas
    assert str(np.sort(tempos)) == "[1 s 2 s 3 s 4 s 5 s 6 s 7 s 8 s 9 s 1,0x10¹ s]"
    tempos.sort()
    assert str(np.sort(tempos)) == "[1 s 2 s 3 s 4 s 5 s 6 s 7 s 8 s 9 s 1,0x10¹ s]"


def test_sorted_python(medidas_desordenadas: NDArray[np.object_]) -> None:
    tempos: NDArray[np.object_] = medidas_desordenadas
    assert (
        str(sorted(tempos))
        == "[1 s, 2 s, 3 s, 4 s, 5 s, 6 s, 7 s, 8 s, 9 s, 1,0x10¹ s]"
    )


def test_medidas_nao_devem_ser_comparaveis():
    x = lab.Medida(5, "", 1)
    y = lab.Medida(6, "", 0.1)
    comparacoes = [lambda x, y: x == y, lambda x, y: x != y]
    for comparacao in comparacoes:
        with pytest.raises(TypeError):
            comparacao(x, y)


def test_medidas_comparacoes():
    x = lab.Medida(1, "", 0.1)
    y = lab.Medida(0.9, "", 0.01)
    z = lab.Medida(50, "", 1)
    w = lab.Medida(45, "", 1)
    assert lab.comparar_medidas(x, y) == lab.Comparacao.EQUIVALENTES
    assert lab.comparar_medidas(x, z) == lab.Comparacao.DIFERENTES
    assert lab.comparar_medidas(z, w) == lab.Comparacao.INCONCLUSIVO

    assert (
        lab.comparar_medidas(x, y, sigma_inferior=0.1, sigma_superior=0.2)
        == lab.Comparacao.DIFERENTES
    )
    assert (
        lab.comparar_medidas(x, z, sigma_inferior=100, sigma_superior=105)
        == lab.Comparacao.EQUIVALENTES
    )

    with pytest.raises(ValueError):
        lab.comparar_medidas(x, y, sigma_inferior=5, sigma_superior=1)
