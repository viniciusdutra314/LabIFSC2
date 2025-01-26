# **LabIFSC2: Cálculos de laboratório com Python**

## Faça propagação de incertezas e conversão de medidas **automaticamente**!

Eis um exemplo simples de uso da biblioteca. Estamos estimando a gravidade da Terra baseado no período de um pêndulo pela conhecida fórmula \(T=2\pi \sqrt{\frac{L}{g}}\):

```py title="Estimativa da gravidade (com LabIFSC2)"
--8<-- "tests/test_doc_gravidade_com_LabIFSC2.py:5:13"
```

\(g=(9,73 \, \pm \, 0,07) \, \frac{\mathrm{m}}{\mathrm{s}^{2}} \)

Podemos copiar o resultado em formato \(\LaTeX\) e adicioná-lo em nosso relatório! Para fins de comparação, este é o código equivalente sem a ajuda da biblioteca. Perceba como, sem a biblioteca, existem muitas possibilidades de erros acidentais:

```py title="Estimativa da gravidade (sem LabIFSC2)"
--8<-- "tests/test_doc_gravidade_sem_LabIFSC2.py:5:14"
```

## O que há de novo?
O LabIFSC2 é uma modernização da biblioteca [LabIFSC](https://github.com/gjvnq/LabIFSC). Os desenvolvedores do LabIFSC2 não são os mesmos do LabIFSC, porém, gostaríamos de deixar aqui nosso agradecimento por terem concebido uma solução tão elegante que agilizou a graduação de várias pessoas.

Mesmo que a interface seja intencionalmente parecida, a implementação é totalmente nova. Para resumir as melhorias, estamos fazendo esta tabela:

| Feature         | LabIFSC       | LabIFSC2      |
|-----------------|---------------|---------------|
| Propagação de erros | Linear      | Arbitrária (Monte Carlo)          |
| Regressões        |   Linear    |  Linear, polinomial, exponencial e lei de potência | 
| Unidades | Implementação autoral | Baseado no famoso [pint](https://pint.readthedocs.io/)
| Constantes da natureza| ❌ | +350 definidas pela [CODATA(2022)](https://codata.org/initiatives/data-science-and-stewardship/fundamental-physical-constants/)
| Operações com arrays| ❌ | Suportadas pelo Numpy 
| Segurança de tipos (mypy)| ❌ | ✅ 
| Docstrings em funções | ❌ | ✅
| Suporte         | ❌ | Ativo         |
| Documentação    | Parcial      | Completa      |

## Instalação
A biblioteca está disponível no PyPI (Python Package Index), então ela pode ser instalada facilmente usando pip. Atualmente, é necessário ter uma versão do Python igual ou superior a 3.10. Para descobrir a versão do seu Python, digite `python --version` no terminal:

```bash
pip install LabIFSC2
```

Recomendamos que você instale o LabIFSC2 em um ambiente virtual. Caso não saiba o que é isso, por favor leia esta [seção](_instalacao.md).

## Escopo
A biblioteca tem a intenção de agilizar cálculos dos laboratórios de física do IFSC da USP de São Carlos:

- Laboratório de Física I
- Laboratório de Física II
- Laboratório de Física III
- Laboratório de Física IV
- Laboratório de Física Avançado
- Laboratório de Física Avançado II

Os critérios de comparação e formatação são baseados na última versão da [apostila I](https://www.ifsc.usp.br/lef/index.php/apostilas/), atualmente a versão 2017 (caso já exista uma versão mais recente, por favor nos avise).

!!! warning
    A propagação de incertezas recomendada pela apostila 1 é somente uma aproximação linear do que seria a propagação exata. Por generalidade e um certo preciosismo do autor, o LabIFSC2 realiza uma propagação por Monte Carlo, que é o que computacionalmente temos de mais próximo do exato.
    
    Por isso, em diversos casos, o LabIFSC (que implementa exatamente a apostila) dará incertezas diferentes do LabIFSC2, geralmente incertezas maiores. Acredito que a maioria dos professores não se importará com isso, visto que é um método mais correto, mas é sempre importante estar ciente disso.

É óbvio que a biblioteca se aplica a outros laboratórios e de outras universidades (principalmente por ter propagação de erros por Monte Carlo). **Só por favor fique atento que talvez certas convenções ou métodos sejam diferentes.**

## Recomendação pessoal
Eu fiz o laboratório I somente com uma calculadora científica, convertendo unidades, propagando os erros derivando na mão, mínimos quadrados usando tabelas e papel milimetrado.

Somente no laboratório II, devido ao [Breno Pelegrin](https://github.com/brenopelegrin), eu comecei a me converter ao mundo da programação e fazer o que eu acredito ser o mais fácil: relatórios em LaTeX  e cálculos em Python (No Google Colab e Overleaf para contribuir em grupo).

Eu acredito que o meu primeiro semestre manual foi muito importante para a minha real compreensão de como esses cálculos são feitos. **Eu sei como essas coisas funcionam**, tanto que consegui fazer uma biblioteca que implementa esses cálculos quase do zero.

A minha recomendação pessoal é que você NÃO utilize esta biblioteca a menos que tenha uma noção de como ela funciona. Eu não quero que, por exemplo, as funções `regressao_linear`, `comparar_medidas`, `intervalo_de_confianca`... sejam coisas mágicas que você utilize sem pensar.

Eu gostaria que ela fosse usada igual ao uso de uma calculadora para realizar operações com números de vários dígitos. **Certamente você sabe como multiplicar `134,5` e `0.215` na mão**, só que não faz sentido perder horas calculando essas coisas se você tem uma calculadora para isso.