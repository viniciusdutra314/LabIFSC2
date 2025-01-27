# **LabIFSC2: Cálculos de laboratório com Python**
<div style="display: flex; gap: 10px;">
    <img src="https://img.shields.io/pypi/pyversions/LabIFSC2">
    <img src="https://img.shields.io/codecov/c/github/viniciusdutra314/LabIFSC2">
    <img src="https://github.com/viniciusdutra314/LabIFSC2/actions/workflows/testes.yaml/badge.svg">
    <img src="https://img.shields.io/github/license/viniciusdutra314/LabIFSC2">

</div>

## Faça propagação de incertezas e conversão de medidas **automaticamente**!

Eis um exemplo simples de uso da biblioteca. Estamos estimando a gravidade da Terra baseado no período de um pêndulo pela conhecida fórmula $T=2\pi \sqrt{\frac{L}{g}}$:

```py title="Estimativa da gravidade (com LabIFSC2)"
from LabIFSC2 import *
pi=constantes.pi
L=Medida(15,'cm',0.1)
T=Medida(780,'ms',1)
gravidade=(4*pi**2)*L/T**2
print(f"{gravidade:si}") #(9,73 ± 0,07) m/s²
print(f"{gravidade:si_latex}") 
'''(9,73 \, \pm \, 0,07) \, 
\frac{\mathrm{m}}{\mathrm{s}^{2}}'''
```

$g=(9,73 \, \pm \, 0,07) \, \frac{\mathrm{m}}{\mathrm{s}^{2}}$

Podemos copiar o resultado em formato $\LaTeX$ e adicioná-lo em nosso relatório!

## O que há de novo?
O LabIFSC2 é uma modernização da biblioteca [LabIFSC](https://github.com/gjvnq/LabIFSC). Os desenvolvedores do LabIFSC2 não são os mesmos do LabIFSC, porém, gostaríamos de deixar aqui nosso agradecimento por terem concebido uma solução tão elegante que agilizou a graduação de várias pessoas.

Mesmo que a interface seja intencionalmente parecida, a implementação é totalmente nova. Para resumir as melhorias, estamos fazendo esta tabela:

| Feature                   | LabIFSC               | LabIFSC2                                                                                                                        |
| ------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Propagação de erros       | Linear                | Arbitrária (Monte Carlo)                                                                                                        |
| Regressões                | Linear                | Linear, polinomial, exponencial e lei de potência                                                                               |
| Unidades                  | Implementação autoral | Baseado no famoso [pint](https://pint.readthedocs.io/)                                                                          |
| Constantes da natureza    | ❌                     | +350 definidas pela [CODATA(2022)](https://codata.org/initiatives/data-science-and-stewardship/fundamental-physical-constants/) |
| Operações com arrays      | ❌                     | Suportadas pelo Numpy                                                                                                           |
| Segurança de tipos (mypy) | ❌                     | ✅                                                                                                                               |
| Docstrings em funções     | ❌                     | ✅                                                                                                                               |
| Suporte                   | ❌                     | Ativo                                                                                                                           |
| Documentação              | Parcial               | Completa                                                                                                                        |

## Instalação
A biblioteca está disponível no PyPI (Python Package Index), então ela pode ser instalada facilmente usando pip. Atualmente, é necessário ter uma versão do Python igual ou superior a 3.10. Para descobrir a versão do seu Python, digite `python --version` no terminal:

```bash
pip install LabIFSC2
```

## Documentação Completa
A documentação completa se encontra tanto no site [readthedocs](https://labifsc2.readthedocs.io/) quanto no [github pages](https://viniciusdutra314.github.io/LabIFSC2/) do projeto