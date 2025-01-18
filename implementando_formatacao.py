from decimal import Decimal, ROUND_HALF_UP
import math
from LabIFSC2 import Medida

def potencia_bonita(exponent: int) -> str:
    superscript_map = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '-': '⁻'
    }
    exponent_str = str(exponent)
    beautiful_exponent = ''.join(superscript_map[char] for char in exponent_str)
    return f"10{beautiful_exponent}"


def formatacao(medida: Medida, fmt_exp: int | bool = False,latex : bool=False) -> str:
    nominal = Decimal(medida.nominal)
    incerteza = Decimal(medida.incerteza)

    og_nominal = math.floor(math.log10(nominal))
    if fmt_exp is False:
        nominal *= Decimal(f"1e{-og_nominal}")
        incerteza *= Decimal(f"1e{-og_nominal}")
    else:
        nominal *= Decimal(f"1e{-fmt_exp}")
        incerteza *= Decimal(f"1e{-fmt_exp}")
    og_incerteza = math.floor(math.log10(incerteza))    
    arred_nominal = nominal.quantize(Decimal(f'1e{og_incerteza}'), rounding=ROUND_HALF_UP)
    arred_incerteza = incerteza.quantize(Decimal(f'1e{og_incerteza}'), rounding=ROUND_HALF_UP)
    arred_nominal_str = str(arred_nominal).replace(".", ",")
    arred_incerteza_str = str(arred_incerteza).replace(".", ",")
    if latex is False:
        unidade = f"{medida._nominal:~P}".split()[1]
    if fmt_exp is False:
        return f"({arred_nominal_str} ± {arred_incerteza_str})x{potencia_bonita(og_nominal)} {unidade}"
    elif og_nominal == 0 or fmt_exp == 0:
        return f"({arred_nominal_str} ± {arred_incerteza_str}) {unidade}"
    else:
        return f"({arred_nominal_str} ± {arred_incerteza_str})x{potencia_bonita(fmt_exp)} {unidade}"
medida=Medida(1.8,0.05,'m')
print(formatacao(medida))
medida.converter_para('cm')
print(formatacao(medida,0))
""" assert formatacao(medida) == "(1.80 ± 0.05) m"
x=Medida(5.34481349,0.03253496,'m')
assert formatacao(x)=='(5.34 ± 0.03) m'
x=Medida(5.34481349,0.00363496,'m')
assert formatacao(x)=="(5.345 ± 0.004) m"
x.converter_para('mm')
assert formatacao(x)=='(5345 ± 4) mm'
volts=Medida(254,1,'mV')
assert formatacao(volts)=='(254 ± 1) mV'
volts.converter_para('V')
print(formatacao(volts,2)) """
#assert formatacao(volts)=='(253 ± 0.001) x 10⁻³ V'



