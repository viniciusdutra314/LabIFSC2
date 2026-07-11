import pytest

import LabIFSC2 as lab


def test_initialization():
    coeficientes = lab.linspaceM(1, 3, 3, "", 0)
    polinomio = lab.AjustePolinomial(coeficientes)
    assert polinomio.grau == 2
    assert polinomio.coef[0].nominal("") == 1
    assert polinomio.coef[1].nominal("") == 2
    assert polinomio.coef[2].nominal("") == 3


def test_call():
    coeficientes = lab.linspaceM(1, 3, 3, "", 0)
    polinomio = lab.AjustePolinomial(coeficientes)
    with pytest.raises(TypeError):
        polinomio(0)
