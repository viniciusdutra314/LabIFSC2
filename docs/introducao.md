## Importação
Como a biblioteca é em português e a maioria das bibliotecas são em inglês, é muito difícil haver algum tipo de conflito de nomes. Então, sinta-se à vontade para fazer:

```py
from LabIFSC2 import *
```

Ou, se não quiser poluir o namespace global, use:

```py
import LabIFSC2 as lab
```

## Classe Medida

A principal classe da biblioteca é a `Medida`. Ela recebe 3 argumentos para sua inicialização[^1]:

- Nominal (\(\mu\)): Valor(es) medido(s).
- Unidade: Unidade da medida (precisa ser a mesma do valor nominal e da incerteza).
- Incerteza (\(\sigma\)): Incerteza experimental.

Para um exemplo prático, consideraremos um tipo de medida comum, o IMC (Índice de Massa Corporal), não confundir com (ICMC). Suponhamos que uma pessoa foi medida (valores fictícios) com uma fita métrica e temos certeza apenas na casa de 1 cm de sua altura e usamos uma balança com precisão de 100 g para medir a sua massa.

Com o LabIFSC2, podemos fazer os cálculos assim:
```py title="Cálculo de IMC"
--8<-- "tests/test_doc_imc.py:5:8"
```
Calculamos então que o IMC tem valor esperado de \(\mu=24,5 \, kg/m²\) e desvio padrão de \(\sigma=0.3 \, kg/m²\).

Você pode acessar o valor nominal e a incerteza fazendo `medida.nominal(unidade)` ou `medida.incerteza(unidade)`. Repare que é necessário especificar uma unidade, visto que o valor nominal/incerteza são totalmente dependentes dela. É importante notar que somente em casos bem específicos você vai acessar diretamente esses valores. Se você usa muito essas funções, talvez não esteja usando a biblioteca corretamente.

```py title="Cálculo de IMC"
--8<-- "tests/test_doc_imc.py:9:10"
```

## Várias medições
Podemos também criar uma medida baseada em várias medições. Imagine que você está medindo o diâmetro de um fio levemente irregular. Você pode preencher o valor nominal como sendo uma lista de medições, a biblioteca irá considerar o valor nominal como a média dos valores.

```py title="Cálculo de IMC"
--8<-- "tests/test_doc_medida_lista.py:7:8"
```
Caso o desvio padrão[^2] das medições seja maior do que a incerteza experimental, então a incerteza é o desvio padrão. Intuitivamente, podemos pensar que o fio é objetivamente irregular e não existe exatamente um raio que o define. 

Mas se a incerteza experimental for maior que o desvio padrão, então não temos certeza se essa variação é devido ao fio ter um formato irregular ou por efeitos aleatórios de medição, a incerteza então é a incerteza experimental. 

Esse comportamento pode ser visto nesse exemplo, preste atenção nas incertezas:

```py title="Cálculo de IMC"
--8<-- "tests/test_doc_medida_lista.py:7:10"
```
## Medidas sem incerteza
É possível criar medidas com incerteza zero. Nesse caso, a biblioteca somente realizará as conversões de unidade. Isso é interessante para um conjunto grande de medidas em que a incerteza é muito pequena, por exemplo, as medidas de voltagem de um osciloscópio, em que a precisão de tempo é enorme. É possível tratar os tempos como exatos, assim um grande ganho em performance é observado, visto que não ocorrerá nenhuma simulação Monte Carlo


## Comparando Medidas
Se uma segunda pessoa afirmar que seu IMC é de (25 ± 0.1), podemos dizer que seus IMCs são equivalentes? Mesmo que \(25 \ne 24.5\), pela incerteza nas medidas podemos dizer que essa diferença está na margem de erro do experimento.

O método que faz essa comparação é `comparar_medidas`, que recebe duas Medidas e retorna se elas são:

- EQUIVALENTES
- DIFERENTES
- INCONCLUSIVO

```py title="Comparando IMC"
--8<-- "tests/test_doc_equivalencia.py:5:8"
```

Perceba que 3 resultados são possíveis, então infelizmente a sintaxe `ìmc1==imc2` ou `ìmc1!=imc2` não é perfeita, porque no caso inconclusivo temos `ìmc1==imc2 (False)` e `ìmc1!=imc2 (False)` ao mesmo tempo, o que creio ser javascript demais pro meu gosto.

O critério usado é o da apostila:

- EQUIVALENTES: \(|\Delta \mu| \le 2(\sigma_1+\sigma_2)\)
- INCONCLUSIVO: \(2(\sigma_1+\sigma_2) < |\Delta \mu| < 3(\sigma_1+\sigma_2)\)
- DIFERENTES: \(|\Delta \mu| \ge 3(\sigma_1+\sigma_2)\)

Intuitivamente, a comparação é feita pelo quanto os valores nominais são diferentes e quanta incerteza temos nas medidas.

## Ordenando Medidas
Em alguns momentos nós queremos usar o `max` ou `min` de um conjunto de medidas. Imagine que você quer, por exemplo, determinar a voltagem/corrente máxima atingida por um circuito.

Mesmo que existam incertezas, geralmente o que você se refere como min,max é em relação ao valor nominal. Então a classe `Medida` implementa comparações < <= > >=, referentes aos valores nominais, assim é possível usar funções do tipo `max`,`min` e `sort` de maneira direta.

```py 
--8<-- "tests/test_doc_sorted_list.py:5:13"
```

## Intervalo de Confiança
Como estamos falando de medidas experimentais, falamos de **intervalos** e não valores exatos. Objetos da classe `Medida` possuem um método chamado `intervalo_de_confiança`. Com ele, podemos especificar uma probabilidade `p` de estarmos representando os valores possíveis das Medidas.

```py title="Intervalo de confiança IMC"
--8<-- "tests/test_doc_intervalo_de_confianca.py:5:7"
```
Basicamente, isso significa que estamos 95% certos de que o IMC está entre \(23,91 \le IMC \le 25,08\). Talvez você esteja surpreso que pelo método de medida temos 1 unidade inteira de IMC podendo variar.

## Convertendo Unidades
Por padrão, a unidade guardada em um objeto `Medida` é a unidade calculada pela operação realizada na sua geração. Então, se tivéssemos medido a altura usando \(cm\), teríamos o IMC em \(kg/cm²\).

Como o LabIFSC2 abstrai a conversão de unidades, uma das escolhas de design da biblioteca foi que a unidade em que a Medida é representada é decidida no momento do print, fazendo o print de uma string formatada, as chamadas [fstrings](https://www.youtube.com/watch?v=fkGFNOOmXsY) (formatted strings) de Python.

```py
print(f"{medida:unidade}")
```

Um exemplo concreto se encontra abaixo:

```py title="Conversão de unidades Medida"
--8<-- "tests/test_doc_imc_cm.py:10:14"
```

## Dimensão
Como unidades só são uma característica do print de uma medida, e não algo intrínseco, uma forma independente de unidade para caracterizar o que uma medida é de fato é sua dimensão. Uma velocidade, por exemplo, independente se está em \(km/h\) ou \(m/s\), é um comprimento dividido por um tempo. Você pode acessar esse atributo com `medida.dimensao`.

```py
--8<-- "tests/test_doc_dimensao.py:5:6"
```

[^1]:
    Perceba que o LabIFSC2 tem uma diferença de ordem de argumentos na criação de uma `Medida` em relação ao LabIFSC. Eu decidi colocar as unidades no meio da declaração pois, pessoalmente, acho que uma unidade no meio dos argumentos torna a leitura dos valores nominais e incerteza mais simples. Isso fica mais evidente em funções como `lab.linspaceM` e `lab.arrayM` em que temos muitos valores numéricos nos seus construtores.
[^2]:
    A convenção de desvio padrão é a mesma da apostila, ou seja, dividimos os desvios quadráticos por \(N-1\) e **NÃO** por \(N\). Isso é chamado de correção de [Bessel](https://en.wikipedia.org/wiki/Bessel%27s_correction). Esse detalhe só tem efeito visível para valores pequenos de \(N\), mas produz um resultado não enviesado para o desvio padrão.