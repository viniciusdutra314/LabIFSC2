from LabIFSC2 import *
from typing import Sequence
class AjustePolinomial:
    """
    Resultado de um ajuste polinomial genérico da forma:
    y = coef[0] + coef[1]*x + coef[2]*x^2 + ... + coef[n]*x^n
    """
    def __init__(self, coeficientes: Sequence[Medida]):
        self.coef = coeficientes
        self.grau = len(coeficientes) - 1

    def __repr__(self) -> str:
        return f"AjustePolinomial(grau={self.grau}, coeficientes={self.coef})"
sum()