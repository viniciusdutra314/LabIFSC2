import math
from decimal import ROUND_HALF_UP, Decimal
from string import Template
from typing import Literal

MAPA_SOBRESCRITO = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

TEMPLATES_MEDIDA: dict[tuple[bool, bool], Template] = {
    (True, False): Template("$nominal$potencia $unidade"),
    (True, True): Template(r"$nominal$potencia \, $unidade"),
    (False, False): Template("($nominal ± $incerteza)$potencia $unidade"),
    (False, True): Template(r"($nominal \, \pm \, $incerteza)$potencia \, $unidade"),
}


def _formatar_medida(
    nominal: float,
    incerteza: float,
    unidade: str,
    expoente: int | None,
    separador_decimal: Literal[".", ","],
    latex: bool,
) -> str:
    """Formata uma medida exata ou com incerteza para texto comum ou LaTeX."""
    if separador_decimal not in {".", ","}:
        raise ValueError("O separador decimal deve ser '.' ou ','")

    valor_nominal = Decimal(str(nominal))
    valor_incerteza = Decimal(str(incerteza))

    match expoente:
        case int(valor):
            expoente = valor
        case None if valor_nominal == 0:
            expoente = 0
        case None:
            expoente = math.floor(abs(valor_nominal).log10())

    match expoente, latex:
        case 0, _:
            potencia = ""
        case valor, True:
            potencia = rf"\times 10^{{{valor}}}"
        case 1, False:
            potencia = " × 10"
        case valor, False:
            potencia = f" × 10{str(valor).translate(MAPA_SOBRESCRITO)}"

    valor_nominal /= Decimal(10) ** expoente
    valor_incerteza /= Decimal(10) ** expoente

    nominal_formatado, incerteza_formatada = _formatar_valores(
        valor_nominal,
        valor_incerteza,
        separador_decimal,
    )

    return (
        TEMPLATES_MEDIDA[(valor_incerteza == 0, latex)]
        .substitute(
            nominal=nominal_formatado,
            incerteza=incerteza_formatada,
            potencia=potencia,
            unidade=unidade,
        )
        .rstrip()
    )


def _formatar_valores(
    nominal: Decimal,
    incerteza: Decimal,
    separador_decimal: Literal[".", ","],
) -> tuple[str, str]:
    """Arredonda o valor nominal na mesma casa decimal da incerteza."""
    if incerteza == 0:
        return (
            _formatar_decimal(
                nominal,
                separador_decimal,
                remover_zeros=True,
            ),
            "",
        )

    casa_incerteza = Decimal(1).scaleb(incerteza.copy_abs().adjusted())
    nominal_arredondado = nominal.quantize(casa_incerteza, rounding=ROUND_HALF_UP)
    incerteza_arredondada = incerteza.quantize(casa_incerteza, rounding=ROUND_HALF_UP)
    return (
        _formatar_decimal(nominal_arredondado, separador_decimal, remover_zeros=False),
        _formatar_decimal(
            incerteza_arredondada, separador_decimal, remover_zeros=False
        ),
    )


def _formatar_decimal(
    valor: Decimal,
    separador_decimal: Literal[".", ","],
    *,
    remover_zeros: bool,
) -> str:
    """Converte um decimal para texto com o separador e os zeros desejados."""
    texto = format(abs(valor) if valor.is_zero() else valor, "f")
    if remover_zeros and "." in texto:
        texto = texto.rstrip("0").rstrip(".")
    return texto.replace(".", separador_decimal)
