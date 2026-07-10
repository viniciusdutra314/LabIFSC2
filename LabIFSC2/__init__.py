"""
LabIFSC2
=====
Biblioteca usada pela graduação do IFSC para os laboratórios de física.
Documentação completa em https://viniciusdutra314.github.io/LabIFSC2/
"""

# ruff: noqa: E402
# Needed to avoid a circular import of MCSamples

MCSamples = 100_000

from ._arrays import arrayM, curva_max, curva_min, incertezas, linspaceM, nominais
from ._medida import Comparacao, Medida, alterar_monte_carlo_samples, comparar_medidas
from ._regressoes import (
    AjusteExponencial,
    AjusteLeiDePotencia,
    AjustePolinomial,
    regressao_exponencial,
    regressao_linear,
    regressao_polinomial,
    regressao_potencia,
)
from .constantes import constantes

__all__ = [
    "arrayM",
    "curva_max",
    "curva_min",
    "incertezas",
    "linspaceM",
    "nominais",
    "Comparacao",
    "Medida",
    "alterar_monte_carlo_samples",
    "comparar_medidas",
    "AjusteExponencial",
    "AjusteLeiDePotencia",
    "AjustePolinomial",
    "regressao_exponencial",
    "regressao_linear",
    "regressao_polinomial",
    "regressao_potencia",
    "constantes",
]
