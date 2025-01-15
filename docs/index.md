# **LabIFSC2: Cálculos de laborátorio com Python**

Olá, seja bem-vindo ao LabIFSC2! Atualmente a **documentação e o código ainda estão sendo escritos**,o que significa que ainda não está configurado perfeitamente para uso

# O que há de novo?
O LabIFSC2 é uma modernização da antiga biblioteca [LabIFSC](https://github.com/gjvnq/LabIFSC), os desenvolvedores do LabIFSC2 não são os mesmos, porém queriamos deixar aqui nosso agradecimento por terem concebido uma solução tão elegante que agilizou a graduação de várias pessoas.


Mesmo que a interface seja intencionalmente parecida a implementação é totalmente nova, para fazermos um resumo das melhorias estamos fazendo essa tabela.


| Feature         | LabIFSC       | LabIFSC2      |
|-----------------|---------------|---------------|
| Propagação de erros | Linear      | Arbitária (Monte Carlo)          |
| Regressões        |   Linear    |  Linear,polinomial,exponencial e lei de potência | 
| Unidades | Implementação autoral | Baseado no famoso [pint](https://pint.readthedocs.io/)
| Constantes da natureza| ❌ | +350  definidas pela [CODATA(2022)](https://codata.org/initiatives/data-science-and-stewardship/fundamental-physical-constants/)
| Suporta Python 2 | ✅ | ❌  
| Operações com arrays| ❌ | Suportadas pelo [Numpy](numpy.org) 
| Tabelas em LaTeX | ❌| ✅ 
| Verificação de tipos| ❌ | ✅ 
| Docstrings em funções | ❌ | ✅
| Suporte         | ❌ | Ativo         |
| Documentação    | Parcial      | Completa      |