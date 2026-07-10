Eu procurei seguir ao máximo o [guia de estilo do sistema métrico](https://metricsystem.net/style-guide/), que, aliás, recomendo a todos que leiam antes de elaborarem seus relatórios. É um material bem explicado e bastante útil. Caso encontrem alguma violação desse estilo, por favor, abram uma issue no repositório para me avisar.

### Ordem de Grandeza  
Por padrão, as medidas serão formatadas seguindo a notação científica, ou seja, a ordem de grandeza será ajustada para que o valor nominal esteja entre 1 e 10. Na maioria dos casos, esse é o comportamento desejado, mas, em algumas situações, podemos querer representar valores como dezenas ou centenas de vezes uma unidade (acima disso, recomenda-se alterar a unidade). Para isso, basta digitar `E` seguido da ordem de grandeza.

```py
--8<-- "tests/test_doc_formatacao.py:5:11"
```  

### Unidades  
Já abordamos um pouco sobre unidades na seção de [introdução](introducao.md#convertendo-unidades). Basicamente, o projeto utiliza a biblioteca [pint](https://pint.readthedocs.io/) para realizar as conversões. Caso desejem saber mais sobre as unidades suportadas e como formatá-las, sugiro que consultem a documentação do Pint. Uma funcionalidade adicional é que, ao digitar `si` na representação de uma medida, ela será exibida no Sistema Internacional (SI).  

De modo geral, é extremamente raro encontrar uma unidade que o Pint não suporte ou não consiga interpretar. Porém, um detalhe importante é que **o Pint é uma biblioteca desenvolvida em inglês**. Assim, se você optar por escrever unidades por extenso (embora eu pessoalmente prefira as abreviações), ele não reconhecerá `metro`, mas sim `meter`.

```py
--8<-- "tests/test_doc_imc_cm.py:10:14"
```  

### LaTeX  
Ao configurar a formatação para LaTeX, o resultado será gerado no formato LaTeX. Embora não seja agradável para leitura humana, será muito útil para o seu Overleaf ou TexLive.  

```py
--8<-- "tests/test_doc_gravidade_com_LabIFSC2.py:10:13"
```  

Para os curiosos, o \(\LaTeX\) renderizado fica assim:  

$$(9,73 \, \pm \, 0,07) \, \frac{\mathrm{m}}{\mathrm{s}^{2}}$$  

### Combinando Formatações  
Para combinar formatações, basta adicionar um underscore `_`. É importante mencionar que a **unidade sempre deve ser especificada antes dos outros formatos**.  

```py
--8<-- "tests/test_doc_combinando_formatacoes.py:5:9"
```