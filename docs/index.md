# **LabIFSC2: Cálculos de laboratório com Python**

## Faça propagação de incertezas e conversão de medidas **automaticamente**!

Eis um exemplo simples de uso da biblioteca, estamos estimando a gravidade da Terra baseado no período de um pêndulo pela conhecida formula \(T=2\pi \sqrt{\frac{L}{g}}\)
```py title="Estimativa da gravidade (com LabIFSC2)"
--8<-- "tests/test_doc_gravidade_com_LabIFSC2.py:5:13"
```

\(g=(9,73 \, \pm \, 0,07) \, 
\frac{\mathrm{m}}{\mathrm{s}^{2}} \)


Podemos copiar o resultado em formato \(\LaTeX\) e adicionarmos em nosso relatório! A fins de comparação esse é o código equivalente sem a ajuda da biblioteca, perceba como sem a biblioteca existem muitas possibilidades de erros acidentais

```py title="Estimativa da gravidade (sem LabIFSC2)"
--8<-- "tests/test_doc_gravidade_sem_LabIFSC2.py:5:14"
```

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
| Segurança de tipos (mypy)| ❌ | ✅ 
| Docstrings em funções | ❌ | ✅
| Suporte         | ❌ | Ativo         |
| Documentação    | Parcial      | Completa      |


## Instalação
A biblioteca está disponível no PyPI(Python Package Index), então ela pode ser instalada facilmente usando pip, atualmente é necessário ter uma versão do python igual ou superior a 3.10, para descobrir a versão do seu python digite `python --version` no terminal
```bash
pip install LabIFSC2
```
Recomendamos você instalar o LabIFSC2 é um ambiente virtual, caso não saiba o que é isso, por favor 
leia essa [secção](_instalacao.md)

## Escopo
A biblioteca tem a intenção de agilizar cálculos dos laboratórios de física do IFSC da USP de São Carlos:

- Laboratório de Física I
- Laboratório de Física II
- Laboratório de Física III
- Laboratório de Física IV
- Laboratório de Física Avançado
- Laboratório de Física Avançado II

Os critérios de comparação e formatação são baseadas na última versão da [apostila I](https://www.ifsc.usp.br/lef/index.php/apostilas/) atualmente a versão 2017 (caso já exista uma versão mais recente por favor nós avise).

!!! warning
    A propagação de incertezas recomendadas pela apostila 1 é somente uma aproximação linear do que seria
    a propagação exata, por generalidade e um certo preciosismo do autor, o LabIFSC2 realiza uma propagação
    por Monte Carlo que seria o que computacionalmente temos o mais próximo de exata.
    
    Por isso, em diversos casos, o LabIFSC (que implementa exatamente a apostila), dará incertezas diferentes do
    LabIFSC2, geralmente incertezas maiores. Acredito que a maioria dos professores não se importaram com isso,
    visto que é um método mais correto, mas é sempre importante estar ciente disso.


É óbvio que a biblioteca se aplica a outros laboratórios e de outras universidades (principalmente por ter propagação de erros por Monte Carlo). 
**Só por favor fique atento que talvez certas convenções ou métodos sejam diferentes**

## Recomendação pessoal
Eu fiz o laboratório I, somente com calculadora científica, convertendo unidades, propagando os erros derivando na mão, mínimos
quadrados usando tabelas e papel milimetrado.

Somente no laboratório II, devido ao [Breno Pelegrin](https://github.com/brenopelegrin) eu comecei a me converter ao mundo da programação, e fazer o que eu acho acredito ser o mais fácil, relatórios em LaTeX (overleaf) e 
cálculos em python (Google colab para fazer em várias pessoas).

Eu acredito que o meu primeiro semestre manual foi muito importante para a minha real compreensão de como esses cálculos
são feitos, **eu sei como essas coisas funcionam**, tanto que eu consegui fazer uma biblioteca que implementa esses cálculos
quase que do zero.

A minha recomendação pessoal é que você NÃO utilize essa biblioteca ao menos que tenha uma noção de como ela funciona,
eu não quero que por exemplo as funções `regressao_linear`,`comparar_medidas`,`intervalo_de_confianca`... Sejam coisas 
mágicas que você utilize sem pensar.

Eu gostaria que ela fosse usada igual ao uso de uma calculadora para realizar operações com números de vários dígitos,
**certamente você sabe como multiplicar `134,5` e `0.215` na mão**, só que não faz sentido perder horas calculando essas coisas,
se você tem uma calculadora para isso.