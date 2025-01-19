# **LabIFSC2: Cálculos de laboratório com Python**

## Faça propagação de incertezas e conversão de medidas **automaticamente**!

Eis um exemplo simples de uso da biblioteca, estamos estimando a gravidade da Terra baseado no período de um pêndulo pela conhecida formula \(T=2\pi \sqrt{\frac{L}{g}}\)
```py title="Estimativa da gravidade (com LabIFSC2)"
--8<-- "tests/test_doc_gravidade_com_LabIFSC2.py:1:12"
```

\(g=(9,73 \, \pm \, 0,07) \, 
\frac{\mathrm{m}}{\mathrm{s}^{2}} \)


Podemos copiar o resultado em formato \(\LaTeX\) e adicionarmos em nosso relatório! A fins de comparação esse é o código equivalente sem a ajuda da biblioteca, perceba como sem a biblioteca existem muitas possibilidades de erros acidentais

```py title="Estimativa da gravidade (sem LabIFSC2)"
--8<-- "tests/test_doc_gravidade_sem_LabIFSC2.py:1:12"
```
## Instalação
A biblioteca está disponível no PyPI(Python Package Index), então ela pode ser instalada facilmente usando pip, atualmente é necessário ter uma versão do python igual ou superior a 3.10, para descobrir a versão do seu python digite `python --version` no terminal
```bash
pip install LabIFSC2
```

## Escopo de aplicação
A biblioteca tem a intenção de agilizar cálculos dos laboratórios de física do IFSC da USP de São Carlos:

- Laboratório de Física I
- Laboratório de Física II
- Laboratório de Física III
- Laboratório de Física IV
- Laboratório de Física Avançado
- Laboratório de Física Avançado II

Os critérios de comparação e formatação são baseadas na última versão da [apostila I](https://www.ifsc.usp.br/lef/index.php/apostilas/) atualmente a versão 2017 (caso já exista uma versão mais recente por favor nós avise).

É óbvio que a biblioteca se aplica a outros laboratórios e de outras universidades (principalmente por ter propagação de erros por Monte Carlo). 
**Só por favor fique atento que talvez certas convenções sejam diferentes**

## O que há de novo?
O LabIFSC2 é uma modernização da antiga biblioteca [LabIFSC](https://github.com/gjvnq/LabIFSC), os desenvolvedores do LabIFSC2 não são os mesmos, porém queríamos deixar aqui nosso agradecimento por terem concebido uma solução tão elegante que agilizou a graduação de várias pessoas.


Mesmo que a interface seja intencionalmente parecida a implementação é totalmente nova, para fazermos um resumo das melhorias estamos fazendo essa tabela.


| Feature         | LabIFSC       | LabIFSC2      |
|-----------------|---------------|---------------|
| Propagação de erros | Linear      | Arbitrária (Monte Carlo)          |
| Regressões        |   Linear    |  Linear,polinomial,exponencial e lei de potência | 
| Unidades | Implementação autoral | Baseado no famoso [pint](https://pint.readthedocs.io/)
| Constantes da natureza| ❌ | +350  definidas pela [CODATA(2022)](https://codata.org/initiatives/data-science-and-stewardship/fundamental-physical-constants/)
| Operações com arrays| ❌ | Suportadas pelo [Numpy](numpy.org) 
| Tabelas em LaTeX | ❌| ✅ 
| Segurança de tipos (mypy)| ❌ | ✅ 
| Docstrings em funções | ❌ | ✅
| Suporte         | ❌ | Ativo         |
| Documentação    | Parcial      | Completa      |