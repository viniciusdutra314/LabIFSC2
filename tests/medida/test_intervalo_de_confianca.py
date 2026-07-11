import mcerp  # type: ignore[import-untyped]
import numpy as np
import pytest
from pint import Quantity

import LabIFSC2 as lab


def criar_distribuicao_multimodal() -> lab.Medida:
    exponencial: lab.Medida = np.exp(  
        lab.Medida(0, "", 1.5) # type: ignore[call-overload]
    )
    return np.sin(exponencial)  # type: ignore[call-overload,no-any-return]


@pytest.mark.parametrize("probabilidade", [0.68, 0.95, 0.997])
def test_intervalo_analitico_coincide_com_percentis_do_mcerp(
    probabilidade: float,
) -> None:
    medida = lab.Medida(120, "cm", 15)
    referencia = mcerp.N(1.2, 0.15)
    percentis = [(1 - probabilidade) / 2, (1 + probabilidade) / 2]

    obtido = medida.intervalo_de_confiança(probabilidade, "m")
    esperado = referencia.percentile(percentis)

    np.testing.assert_allclose(obtido, esperado, rtol=2e-3, atol=2e-3)


@pytest.mark.parametrize("probabilidade", [0.5, 0.9, 0.99])
def test_intervalo_amostral_coincide_com_mcerp_para_distribuicao_normal(
    probabilidade: float,
) -> None:
    medida = lab.Medida(2, "s", 0.3)
    _ = medida.histograma
    referencia = mcerp.N(2, 0.3)
    percentis = [(1 - probabilidade) / 2, (1 + probabilidade) / 2]

    obtido = medida.intervalo_de_confiança(probabilidade, "s")
    esperado = referencia.percentile(percentis)

    np.testing.assert_allclose(obtido, esperado, rtol=2e-2, atol=2e-2)


def test_intervalo_amostral_nao_modifica_histograma() -> None:
    medida = lab.Medida(2, "m", 0.3)
    histograma = medida.histograma
    assert isinstance(histograma, Quantity)
    unidade_original = histograma.units
    amostras_originais = np.asarray(histograma.magnitude).copy()

    medida.intervalo_de_confiança(0.95, "cm")

    histograma_depois = medida.histograma
    assert isinstance(histograma_depois, Quantity)
    assert histograma_depois.units == unidade_original
    np.testing.assert_array_equal(histograma_depois.magnitude, amostras_originais)


@pytest.mark.parametrize("probabilidade", [0.01, 0.5, 0.95, 0.99999])
def test_intervalo_amostral_contem_probabilidade_em_distribuicao_multimodal(
    probabilidade: float,
) -> None:
    medida = criar_distribuicao_multimodal()

    limite_inferior, limite_superior = medida.intervalo_de_confiança(probabilidade, "")
    probabilidade_obtida = medida.probabilidade_de_estar_entre(
        limite_inferior, limite_superior, ""
    )

    assert probabilidade_obtida == pytest.approx(probabilidade, abs=1e-5)

def test_intervalo_de_medida_exata_e_degenerado_na_unidade_solicitada() -> None:
    medida = lab.Medida(2, "m")
    assert medida.intervalo_de_confiança(0.95, "cm") == (200, 200)


@pytest.mark.parametrize("probabilidade", [-1, 0, 1, 1.1, np.nan])
def test_intervalo_rejeita_probabilidade_fora_do_intervalo_aberto(
    probabilidade: float,
) -> None:
    with pytest.raises(ValueError, match="entre 0 e 1"):
        lab.Medida(0, "s", 1).intervalo_de_confiança(probabilidade, "s")


def test_intervalo_rejeita_unidade_incompativel() -> None:
    with pytest.raises(ValueError, match="não é compatível"):
        lab.Medida(0, "m", 1).intervalo_de_confiança(0.95, "s")


@pytest.mark.parametrize(
    ("limite_inferior", "limite_superior", "esperado"),
    [(-1, 1, 0.682689), (-2, 2, 0.9545), (-3, 3, 0.9973)],
)
def test_probabilidade_analitica_da_normal(
    limite_inferior: float,
    limite_superior: float,
    esperado: float,
) -> None:
    medida = lab.Medida(0, "mm", 1)

    assert medida.probabilidade_de_estar_entre(
        limite_inferior, limite_superior, "mm"
    ) == pytest.approx(esperado, rel=1e-4)


def test_probabilidade_rejeita_intervalo_invertido_e_unidade_incompativel() -> None:
    medida = lab.Medida(0, "m", 1)

    with pytest.raises(ValueError, match="a deve ser menor"):
        medida.probabilidade_de_estar_entre(1, -1, "m")
    with pytest.raises(ValueError, match="não é compatível"):
        medida.probabilidade_de_estar_entre(-1, 1, "s")
