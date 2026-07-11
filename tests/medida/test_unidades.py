from collections.abc import Callable
from typing import cast

import numpy as np
import pint
import pytest

import LabIFSC2 as lab


@pytest.fixture(scope="module")
def ureg_referencia() -> pint.UnitRegistry[float]:
    return pint.UnitRegistry()


@pytest.mark.parametrize(
    ("valor", "origem", "destino"),
    [
        (1, "m", "cm"),
        (1, "km/h", "m/s"),
        (1, "J", "kg*m^2/s^2"),
        (180, "degree", "radian"),
        (1, "liter", "m^3"),
        (1, "micrometer", "nm"),
    ],
)
def test_nominal_e_incerteza_seguem_conversoes_do_pint(
    ureg_referencia: pint.UnitRegistry[float],
    valor: float,
    origem: str,
    destino: str,
) -> None:
    medida = lab.Medida(valor, origem, valor / 10)
    nominal_esperado = ureg_referencia.Quantity(valor, origem).to(destino).magnitude
    incerteza_esperada = abs(
        ureg_referencia.Quantity(valor / 10, origem).to(destino).magnitude
    )

    assert medida.nominal(destino) == pytest.approx(nominal_esperado)
    assert medida.incerteza(destino) == pytest.approx(incerteza_esperada)
    assert (
        medida.dimensao
        == ureg_referencia.Quantity(0, origem).to(destino).dimensionality
    )


@pytest.mark.parametrize(
    ("unidade", "unidade_base"),
    [("cm", "m"), ("hour", "s"), ("N", "kg*m/s^2"), ("bar", "kg/m/s^2")],
)
def test_conversao_si_segue_unidades_base_do_pint(
    ureg_referencia: pint.UnitRegistry[float],
    unidade: str,
    unidade_base: str,
) -> None:
    medida = lab.Medida(2, unidade, 0.1)
    esperado = ureg_referencia.Quantity(2, unidade).to(unidade_base).magnitude

    assert medida.nominal("si") == pytest.approx(esperado)


def test_soma_converte_unidades_compativeis() -> None:
    metros = lab.Medida(10, "m", 1)
    centimetros = lab.Medida(55, "cm", 0.1)
    resultado = metros + centimetros
    assert resultado.nominal("m") == pytest.approx(10.55)
    assert resultado.incerteza("m") == pytest.approx(np.hypot(1, 0.001))


def test_soma_de_angulos_converte_graus_e_radianos(
    ureg_referencia: pint.UnitRegistry[float],
) -> None:
    resultado = lab.Medida(45, "degree", 0.01) + lab.Medida(1, "radian", 0.01)
    esperado = cast(
        pint.Quantity[float],
        ureg_referencia.Quantity(45, "degree") + ureg_referencia.Quantity(1, "radian"),
    )
    assert resultado.nominal("degree") == pytest.approx(esperado.to("degree").magnitude)
    assert resultado.nominal("radian") == pytest.approx(esperado.to("radian").magnitude)


def test_multiplicacao_compoe_unidades() -> None:
    resultado = lab.Medida(3, "N", 0.01) * lab.Medida(2, "m", 0.01)

    assert resultado.nominal("J") == pytest.approx(6, rel=1e-3)
    assert resultado.dimensao == lab.Medida(1, "J").dimensao


@pytest.mark.parametrize("operacao", [lambda x, y: x + y, lambda x, y: x - y])
def test_soma_e_subtracao_rejeitam_dimensoes_incompativeis(
    operacao: Callable[[lab.Medida, lab.Medida], lab.Medida],
) -> None:
    with pytest.raises(ValueError, match="não é possível"):
        operacao(lab.Medida(10, "m", 1), lab.Medida(10, "s", 1))


@pytest.mark.parametrize("funcao", [np.sin, np.cos, np.tan])
def test_funcoes_trigonometricas_rejeitam_dimensao_nao_angular(
    funcao: Callable[[lab.Medida], lab.Medida],
) -> None:
    with pytest.raises(pint.DimensionalityError):
        funcao(lab.Medida(45, "m", 1))


@pytest.mark.parametrize(
    ("funcao", "angulo", "esperado"),
    [(np.sin, 30, 0.5), (np.cos, 60, 0.5), (np.tan, 45, 1.0)],
)
def test_funcoes_trigonometricas_aceitam_angulos_e_removem_unidade(
    funcao: Callable[[lab.Medida], lab.Medida],
    angulo: float,
    esperado: float,
) -> None:
    resultado = funcao(lab.Medida(angulo, "degree"))

    assert resultado.nominal("") == pytest.approx(esperado)
    assert resultado.dimensao == lab.Medida(1, "").dimensao


@pytest.mark.parametrize("funcao", [np.exp, np.log, np.log2, np.log10])
def test_funcoes_exponenciais_e_logaritmicas_exigem_adimensional(
    funcao: Callable[[lab.Medida], lab.Medida],
) -> None:
    with pytest.raises(pint.DimensionalityError):
        funcao(lab.Medida(1, "m", 0.01))


@pytest.mark.parametrize(("origem", "destino"), [("m/s", "km/h"), ("km/h", "m/s")])
def test_conversao_de_array_coincide_com_pint(
    ureg_referencia: pint.UnitRegistry[float],
    origem: str,
    destino: str,
) -> None:
    valores = np.array([0, 1, 2, 5], dtype=float)
    medidas = lab.arrayM(valores, origem, 0.01)
    esperado = ureg_referencia.Quantity(valores, origem).to(destino).magnitude

    obtido = lab.nominais(medidas, destino)

    assert isinstance(obtido, np.ndarray)
    np.testing.assert_allclose(obtido, esperado)


def test_conversao_para_unidade_incompativel_propaga_erro_do_pint() -> None:
    medida = lab.Medida(1, "m", 0.1)
    with pytest.raises(pint.DimensionalityError):
        medida.nominal("s")
    with pytest.raises(pint.DimensionalityError):
        medida.incerteza("s")
