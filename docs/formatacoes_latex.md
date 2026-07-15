Eu procurei seguir ao máximo o [guia de estilo do sistema métrico](https://metricsystem.net/style-guide/), que, aliás, recomendo a todos que leiam antes de elaborarem seus relatórios. É um material bem explicado e bastante útil. Caso encontrem alguma violação desse estilo, por favor, abram uma issue no repositório para me avisar.

### Ordem de Grandeza

Por padrão, as medidas serão formatadas seguindo a notação científica, ou seja, a ordem de grandeza será ajustada para que o valor nominal esteja entre 1 e 10. Na maioria dos casos, esse é o comportamento desejado, mas, em algumas situações, podemos querer representar valores como dezenas ou centenas de vezes uma unidade (acima disso, recomenda-se alterar a unidade). Para isso, passe a ordem de grandeza desejada no argumento `expoente` de `fmt`.

```py
--8<-- "tests/doctest/test_doc_formatacao.py:formatacao"
```

### Unidades

Já abordamos um pouco sobre unidades na seção de [introdução](introducao.md#convertendo-unidades). Basicamente, o projeto utiliza a biblioteca [pint](https://pint.readthedocs.io/) para realizar as conversões. Caso desejem saber mais sobre as unidades suportadas e como formatá-las, sugiro que consultem a documentação do Pint. Uma funcionalidade adicional é passar `unidade="si"` para exibir uma medida no Sistema Internacional (SI).

De modo geral, é extremamente raro encontrar uma unidade que o Pint não suporte ou não consiga interpretar. Porém, um detalhe importante é que **o Pint é uma biblioteca desenvolvida em inglês**. Assim, se você optar por escrever unidades por extenso (embora eu pessoalmente prefira as abreviações), ele não reconhecerá `metro`, mas sim `meter`.

```py
--8<-- "tests/doctest/test_doc_imc_cm.py:imc_unidades"
```

### LaTeX

Ao passar `latex=True` para `fmt`, o resultado será gerado no formato LaTeX. Embora não seja agradável para leitura humana, será muito útil para o seu Overleaf ou TexLive.

```py
--8<-- "tests/doctest/test_doc_gravidade_com_LabIFSC2.py:gravidade_latex"
```

Para os curiosos, o \(\LaTeX\) renderizado fica assim:

$$(9,73 \, \pm \, 0,07) \, \frac{\mathrm{m}}{\mathrm{s}^{2}}$$

### Combinando Formatações

As opções podem ser combinadas usando argumentos nomeados na mesma chamada de `fmt`.

```py
--8<-- "tests/doctest/test_doc_combinando_formatacoes.py:formatacoes_combinadas"
```
