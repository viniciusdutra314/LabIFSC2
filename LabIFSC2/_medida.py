from __future__ import annotations

import operator
from collections.abc import Callable, Iterable
from enum import Enum
from numbers import Real
from statistics import NormalDist
from typing import Literal, cast, overload

import numpy as np
from numpy.typing import NDArray
from pint import Quantity, UnitRegistry
from pint.util import UnitsContainer

from . import MCSamples
from ._fmt import _formatar_medida

_gerador_monte_carlo = np.random.default_rng()


def alterar_monte_carlo_samples(novo_valor: int) -> None:
    global MCSamples
    if novo_valor <= 0:
        raise ValueError("MCSamples deve ser maior que 0")
    MCSamples = novo_valor


def alterar_monte_carlo_rng(novo_gerador: np.random.Generator) -> None:
    """Altera o gerador aleatório usado nas simulações de Monte Carlo.

    Args:
        novo_gerador: Gerador aleatório usado nas próximas simulações.

    Raises:
        TypeError: Se o valor não for um ``numpy.random.Generator``.
    """
    global _gerador_monte_carlo
    if not isinstance(novo_gerador, np.random.Generator):
        raise TypeError("O gerador deve ser uma instância de numpy.random.Generator")
    _gerador_monte_carlo = novo_gerador


ureg: UnitRegistry[float] = UnitRegistry()

HistogramaType = (
    Quantity[NDArray[np.float64]] | Quantity[float] | float | NDArray[np.float64]
)


FUNCOES_NUMPY_SUPORTADAS = frozenset(
    {
        "sin",
        "cos",
        "exp",
        "sqrt",
        "sinh",
        "cosh",
        "tanh",
        "arcsinh",
        "arccosh",
        "arctanh",
        "cbrt",
        "tan",
        "arcsin",
        "arccos",
        "arctan",
        "log",
        "log2",
        "log10",
    }
)

OPERACOES_UFUNC_UNARIAS: dict[str, Callable[[Medida], Medida]] = {
    "positive": operator.pos,
    "negative": operator.neg,
    "absolute": operator.abs,
    "fabs": operator.abs,
}

OPERACOES_UFUNC_BINARIAS: dict[str, Callable[[object, object], object]] = {
    "add": operator.add,
    "subtract": operator.sub,
    "multiply": operator.mul,
    "divide": operator.truediv,
    "true_divide": operator.truediv,
    "power": operator.pow,
}


def montecarlo(  # type: ignore[explicit-any]
    func: Callable[..., HistogramaType], *params: Medida
) -> Medida:
    x_samples: list[HistogramaType] = [parametro.histograma for parametro in params]
    histograma = func(*x_samples)
    mean = np.mean(histograma)
    std = np.std(histograma, mean=mean)
    if isinstance(histograma, Quantity):
        mean_q = cast(Quantity[float], mean)
        std_q = cast(Quantity[float], std)
        resultado = Medida(mean_q.magnitude, str(histograma.units), std_q.magnitude)
    else:
        resultado = Medida(float(mean), "", float(std))
    resultado._histograma = histograma
    return resultado


class Medida:
    @overload
    def __init__(self, nominal: float, unidade: str, incerteza: float = 0): ...

    @overload
    def __init__(
        self, nominal: Iterable[float], unidade: str, incerteza: float = 0
    ): ...

    def __init__(
        self, nominal: float | Iterable[float], unidade: str, incerteza: float = 0
    ):
        """
        Inicializa uma instância da classe com valores nominais, unidade e incerteza.

        Args:
            nominal (float | Iterable[float]): Valor nominal ou uma coleção de
            valores nominais.
            unidade (str): Unidade de medida.
            incerteza (float): Incerteza associada ao valor nominal.

        Raises:
            ValueError: Se a incerteza for negativa.
            ValueError: Se a sequência de medidas tiver menos de 2 elementos.
        """

        if incerteza < 0:
            raise ValueError("Incerteza não pode ser negativa")
        if isinstance(nominal, Iterable):
            nominal = list(nominal)
            if len(nominal) < 2:
                raise ValueError("Lista de medidas deve ter pelo menos 2 elementos")
            mean = np.mean(nominal)

            std = np.std(nominal, ddof=1, mean=mean)
            self._nominal = ureg.Quantity(mean, unidade).to_reduced_units()
            self._incerteza = ureg.Quantity(
                std if std > incerteza else incerteza, unidade
            ).to_reduced_units()
        else:
            self._nominal = ureg.Quantity(nominal, unidade).to_reduced_units()
            self._incerteza = ureg.Quantity(incerteza, unidade).to_reduced_units()
        self._histograma: HistogramaType | None = None

    def nominal(self: Medida, unidade: str) -> float:
        """
        Retorna o valor nominal da medida na unidade especificada.

        Args:
            unidade (str): A unidade na qual o valor nominal deve ser retornado.
            'si', retorna o valor em unidades do Sistema Internacional (SI).

        Returns:
            float: O valor nominal da medida na unidade especificada.
        """

        if unidade.lower() == "si":
            return float(self._nominal.to_base_units().magnitude)
        else:
            return float(self._nominal.to(unidade).magnitude)

    def incerteza(self: Medida, unidade: str) -> float:
        """
        Retorna a incerteza da medida na unidade especificada.

        Args:
            unidade (str): A unidade na qual a incerteza deve ser retornado.
            'si' retorna o valor em unidades do Sistema Internacional (SI).

        Returns:
            float: O valor da incerteza da medida na unidade especificada.
        """
        if unidade.lower() == "si":
            return float(self._incerteza.to_base_units().magnitude)
        else:
            return float(self._incerteza.to(unidade).magnitude)

    @property
    def dimensao(self: Medida) -> UnitsContainer:
        return self._nominal.dimensionality

    @property
    def histograma(self: Medida) -> HistogramaType:
        if self._histograma is None:
            if self._incerteza.magnitude != 0:
                self._histograma = cast(
                    Quantity[NDArray[np.float64]],
                    (
                        _gerador_monte_carlo.normal(
                            self._nominal.magnitude,
                            self._incerteza.magnitude,
                            size=MCSamples,
                        )
                        * self._nominal.units
                    ),
                )
            else:
                self._histograma = cast(Quantity[float], self._nominal)
        return self._histograma

    def fmt(
        self,
        unidade: str | None = None,
        expoente: int | None = None,
        latex: bool = False,
        separador_decimal: Literal[".", ","] = ",",
    ) -> str:
        """Formata a medida para uma string.

        Args:
            unidade: Unidade usada no resultado. Por padrão, mantém a unidade da
                medida. O valor ``"si"`` converte a medida para unidades do SI.
            expoente: Expoente da potência usada para escalar o valor. Quando
                omitido, valores maiores ou iguais a 10 são normalizados.
            separador_decimal: Caractere usado como separador decimal.
            latex: Indica se o resultado deve usar sintaxe LaTeX.

        Returns:
            Medida formatada para exibição.

        Raises:
            ValueError: Se o separador decimal for inválido.
        """
        match unidade:
            case None:
                nominal, incerteza = self._nominal, self._incerteza
            case str(valor) if valor.lower() == "si":
                nominal = self._nominal.to_base_units()
                incerteza = self._incerteza.to_base_units()
            case str(valor):
                nominal = self._nominal.to(valor)
                incerteza = self._incerteza.to(valor)

        unidade_formatada = f"{nominal.units:~L}" if latex else f"{nominal.units:~P}"
        return _formatar_medida(
            nominal=float(nominal.magnitude),
            incerteza=float(incerteza.magnitude),
            unidade=unidade_formatada,
            expoente=expoente,
            separador_decimal=separador_decimal,
            latex=latex,
        )

    def __str__(self) -> str:
        return self.fmt()

    def __repr__(self) -> str:
        return self.fmt()

    def __array_ufunc__(
        self,
        ufunc: np.ufunc,
        method: Literal["__call__", "reduce", "reduceat", "accumulate", "outer", "at"],
        *inputs: object,
        **kwargs: object,
    ) -> object:
        if method != "__call__" or kwargs:
            return NotImplemented

        nome = ufunc.__name__
        funcao_matematica = nome in FUNCOES_NUMPY_SUPORTADAS
        op_unary = OPERACOES_UFUNC_UNARIAS.get(nome)
        op_binary = OPERACOES_UFUNC_BINARIAS.get(nome)
        has_array = any(isinstance(entrada, np.ndarray) for entrada in inputs)

        match inputs:
            case (Medida() as medida,) if funcao_matematica:
                return montecarlo(ufunc, medida)
            case (Medida() as medida,) if op_unary:
                return op_unary(medida)
            case (l, r) if op_binary and has_array:
                return np.vectorize(op_binary, otypes=[object])(l, r)
            case (l, r) if op_binary:
                return op_binary(l, r)
            case _:
                return NotImplemented

    def __getattr__(self, func_name: str) -> Callable[[], Medida]:
        if func_name not in FUNCOES_NUMPY_SUPORTADAS:
            raise AttributeError
        func = getattr(np, func_name)

        def funcao_recebe_medida() -> Medida:
            return montecarlo(func, self)

        return funcao_recebe_medida

    """Essas funções de comparação são necessárias para que max,min ou
    np.max,np.min funcionem com medidas do jeito esperado (comparar o valor nominal)
    Repare que não há implementação == e !=, use a função comparar_medidas.
    """

    def __eq__(self, outro: object) -> bool:
        raise TypeError(
            '"Como a comparação entre Medidas pode gerar três resultados \
    diferentes: iguais, diferentes, ou inconclusivo, optamos por \
    fazer uma função separada \
    chamada compara_medidas(x:Medida,y:Medida) -> [Iguais | Diferentes | Inconclusivo]"'
        )

    def __ne__(self, outro: object) -> bool:
        raise TypeError(
            '"Como a comparação entre Medidas pode gerar três resultados \
    diferentes: iguais, diferentes, ou inconclusivo, \
    optamos por fazer uma função separada \
    chamada compara_medidas(x:Medida,y:Medida) -> [Iguais | Diferentes | Inconclusivo]"'
        )

    def __le__(self, outro: object) -> bool:
        return (
            self._nominal <= outro._nominal
            if isinstance(outro, Medida)
            else NotImplemented
        )

    def __lt__(self, outro: object) -> bool:
        return (
            self._nominal < outro._nominal
            if isinstance(outro, Medida)
            else NotImplemented
        )

    def __ge__(self, outro: object) -> bool:
        return (
            self._nominal >= outro._nominal
            if isinstance(outro, Medida)
            else NotImplemented
        )

    def __gt__(self, outro: object) -> bool:
        return (
            self._nominal > outro._nominal
            if isinstance(outro, Medida)
            else NotImplemented
        )

    def __add__(self: Medida, outro: Medida | float) -> Medida:
        if isinstance(outro, Real):
            nova_medida = Medida(
                self._nominal.magnitude + outro,
                str(self._nominal.units),
                self._incerteza.magnitude,
            )
            if self._histograma is not None:
                nova_medida._histograma = self._histograma + (
                    outro * self._nominal.units
                )
            return nova_medida
        elif isinstance(outro, Medida):
            if self._nominal.is_compatible_with(outro._nominal):
                if self is outro:
                    return 2 * self
                elif self._histograma is None and outro._histograma is None:
                    # Como existe solução analítica da soma entre duas gaussianas
                    # iremos usar esse resultado para otimizar o código
                    media = self._nominal + outro._nominal
                    desvio_padrao = (self._incerteza**2 + outro._incerteza**2) ** (
                        1 / 2
                    )
                    desvio_padrao.ito(media.units)
                    return Medida(
                        media.magnitude, str(media.units), desvio_padrao.magnitude
                    )
                else:
                    return montecarlo(lambda x, y: x + y, self, outro)
            else:
                raise ValueError(
                    f"A soma entre {self._nominal.dimensionality} e"
                    f" {outro._nominal.dimensionality} não é possível"
                )
        else:
            return NotImplemented

    def __sub__(self: Medida, outro: Medida | float) -> Medida:
        if self is outro:
            return Medida(0, str(self._nominal.units), 0)
        return self + (-outro)

    def __mul__(self: Medida, outro: Medida | float) -> Medida:
        if self is outro:
            return montecarlo(lambda x: x**2, self)
        if isinstance(outro, Medida):
            return montecarlo(lambda x, y: x * y, self, outro)
        elif isinstance(outro, Real):
            resultado = Medida(
                self._nominal.magnitude * outro,
                str(self._nominal.units),
                abs(self._incerteza.magnitude * outro),
            )
            if self._histograma is not None:
                resultado._histograma = self._histograma * outro
            return resultado
        else:
            return NotImplemented

    def __truediv__(self: Medida, outro: Medida | float) -> Medida:
        if self is outro:
            return Medida(1, "", 0)
        if isinstance(outro, Medida):
            return montecarlo(lambda x, y: x / y, self, outro)
        elif isinstance(outro, Real):
            resultado = Medida(
                self._nominal.magnitude / outro,
                str(self._nominal.units),
                self._incerteza.magnitude / abs(outro),
            )
            if self._histograma is not None:
                resultado._histograma = cast(HistogramaType, self._histograma / outro)
            return resultado
        else:
            return NotImplemented

    def __rtruediv__(self: Medida, outro: float) -> Medida:
        if isinstance(outro, Real):
            return montecarlo(lambda x: outro / x, self)
        else:
            return NotImplemented

    def __pow__(self: Medida, outro: Medida | float) -> Medida:
        if isinstance(outro, Medida):
            return montecarlo(lambda x, y: x**y, self, outro)
        elif isinstance(outro, Real):
            return montecarlo(lambda x: np.power(x, outro), self)
        else:
            return NotImplemented

    def __rpow__(self: Medida, outro: float) -> Medida:
        if isinstance(outro, Real):
            return montecarlo(lambda x: np.power(outro, x), self)
        else:
            return NotImplemented

    def __radd__(self: Medida, outro: Medida | float) -> Medida:
        return self.__add__(outro)

    def __rsub__(self: Medida, outro: Medida | float) -> Medida:
        return (-self) + outro

    def __rmul__(self: Medida, outro: Medida | float) -> Medida:
        return self.__mul__(outro)

    def __abs__(self: Medida) -> Medida:
        resultado = Medida(
            abs(self._nominal.magnitude),
            str(self._nominal.units),
            self._incerteza.magnitude,
        )
        if self._histograma is not None:
            resultado._histograma = cast(HistogramaType, abs(self._histograma))
        return resultado

    def __neg__(self: Medida) -> Medida:
        resultado = Medida(
            -(self._nominal.magnitude),
            str(self._nominal.units),
            self._incerteza.magnitude,
        )
        if self._histograma is not None:
            resultado._histograma = cast(HistogramaType, -self._histograma)
        return resultado

    def __pos__(self) -> Medida:
        resultado = Medida(
            self._nominal.magnitude,
            str(self._nominal.units),
            self._incerteza.magnitude,
        )
        if self._histograma is not None:
            resultado._histograma = self._histograma
        return resultado

    def probabilidade_de_estar_entre(self, a: float, b: float, unidade: str) -> float:
        """
        Calcula a probabilidade de uma medida estar entre dois valores especificados.

        Args:
            a (float): O valor inferior do intervalo.
            b (float): O valor superior do intervalo.
            unidade (str): A unidade de medida dos valores a e b.

        Returns:
            float: A probabilidade de a medida estar entre os valores a e b.

        Raises:
            ValueError: Se o valor de `a` for maior que `b`.
            ValueError: Se a unidade fornecida não for compatível
            com a unidade da medida.
        """
        if a > b:
            raise ValueError("a deve ser menor que b")
        if not self._nominal.is_compatible_with(unidade):
            raise ValueError(
                f"Unidade {unidade} não é compatível com a unidade da medida"
            )

        if self._histograma is None:
            # estamos resolvendo de maneira análitica
            mu = self._nominal.to(unidade).magnitude
            sigma = self._incerteza.to(unidade).magnitude
            gaussiana = NormalDist(mu, sigma)
            return gaussiana.cdf(float(b)) - gaussiana.cdf(float(a))
        else:
            a_quantidade = ureg.Quantity(a, unidade)
            b_quantidade = ureg.Quantity(b, unidade)
            probabilidade = np.mean(
                (self._histograma >= a_quantidade) & (self._histograma <= b_quantidade),
                dtype=float,
            )
            return float(probabilidade)

    def intervalo_de_confiança(
        self: Medida, p: float, unidade: str
    ) -> tuple[float, float]:
        """
        Calcula o intervalo de confiança para a medida.

        Args:
            p (float): Probabilidade associada ao intervalo de confiança (0,1)
            unidade (str): Unidade de medida para o intervalo de confiança.

        Returns:
                tuple: Tupla [limite-inferior, limite-superior].

        Raises:
            ValueError: Se `p` não estiver entre 0 e 1.
        """

        if not 0 < float(p) < 1:
            raise ValueError("p deve estar entre 0 e 1 (exclusivo)")
        if not self._nominal.is_compatible_with(unidade):
            raise ValueError(
                f"Unidade {unidade} não é compatível com a unidade da medida"
            )

        if self._histograma is None:
            # estamos resolvendo de maneira analítica
            mu = self._nominal.to(unidade).magnitude
            sigma = self._incerteza.to(unidade).magnitude
            if sigma == 0:
                return (float(mu), float(mu))
            gaussiana = NormalDist(mu, sigma)
            limite_inferior = gaussiana.inv_cdf((1 - float(p)) / 2)
            limite_superior = gaussiana.inv_cdf((1 + float(p)) / 2)
            return (limite_inferior, limite_superior)
        else:
            h_q = cast(Quantity[NDArray[np.float64]], self.histograma)
            magnitudes = np.sort(np.asarray(h_q.to(unidade).magnitude))
            num_elements = len(magnitudes)
            selected_elements = max(1, int(np.ceil(float(p) * num_elements)))
            intervals = (
                magnitudes[selected_elements - 1 :]
                - magnitudes[: num_elements - selected_elements + 1]
            )

            shortest_interval_index = np.argmin(intervals)
            shortest_interval = (
                float(magnitudes[shortest_interval_index]),
                float(magnitudes[shortest_interval_index + selected_elements - 1]),
            )
            return shortest_interval


class Comparacao(Enum):
    EQUIVALENTES = "iguais"
    DIFERENTES = "diferentes"
    INCONCLUSIVO = "inconclusivo"


def comparar_medidas(
    medida1: Medida,
    medida2: Medida,
    sigma_inferior: float = 2,
    sigma_superior: float = 3,
) -> Comparacao:
    """
    Compara duas medidas considerando suas incertezas e
    retorna o resultado da comparação.

    Args:
        medida1 (Medida): A primeira medida a ser comparada.
        medida2 (Medida): A segunda medida a ser comparada.
        sigma_inferior (float, opcional): O fator sigma inferior para
        considerar as medidas equivalentes. Default é 2.
        sigma_superior (float, opcional): O fator sigma superior para
        considerar as medidas diferentes. Default é 3.

    Returns:
        Comparacao: O resultado da comparação, que pode ser
        EQUIVALENTES, DIFERENTES ou INCONCLUSIVO.

    Raises:
        ValueError: Se o sigma_inferior for maior que o sigma_superior.
    """

    diferenca_nominal = abs(medida1 - medida2).nominal("si")
    soma_incertezas = medida1.incerteza("si") + medida2.incerteza("si")
    if sigma_inferior > sigma_superior:
        raise ValueError(
            "Sigma para serem consideradas iguais é maior que o sigma \
para serem diferentes"
        )

    if diferenca_nominal < sigma_inferior * soma_incertezas:
        return Comparacao.EQUIVALENTES
    elif diferenca_nominal > sigma_superior * soma_incertezas:
        return Comparacao.DIFERENTES
    else:
        return Comparacao.INCONCLUSIVO
