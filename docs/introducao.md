## Importação
Como a biblioteca será usada na maioria dos casos para códigos pequenos, não vejo problema em importar a biblioteca para o namespace global. Então, sinta-se à vontade para fazer:

```py
from LabIFSC2 import *
```

Ou, se não quiser sujar o namespace global, use:

```py
import LabIFSC2 as lab
```

Só não importe globalmente outra biblioteca numérica como o numpy, caso contrário, haverá conflitos de nomes (lab.sin, np.sin,lab.linspace,np.linspace...).

## Classe Medida
A principal classe da biblioteca é a `Medida`. Ela recebe 3 argumentos para sua inicialização:

- Nominal (\(\mu\)): Valor medido ou média dos valores medidos.
- Incerteza (\(\sigma\)): Incerteza experimental ou dispersão das medidas.
- Unidade: Unidade da medida (precisa ser a mesma do valor nominal e da incerteza).

Para um exemplo prático, consideraremos um tipo de medida comum, o IMC (não confundir com ICMC). Suponhamos que uma pessoa foi medida (valores fictícios) com uma fita métrica e temos certeza apenas na casa de 1 cm, e usamos uma balança com precisão de 100 g.

Com o LabIFSC2, podemos fazer os cálculos assim:

```py title="Cálculo de IMC"
--8<-- "tests/test_doc_imc.py:5:8"
```
Calculamos então que o IMC tem valor esperado de \(\mu=24,5 \, kg/m²\) e desvio padrão de \(\sigma=0.3 \, kg/m²\).

Você pode acessar o valor nominal e a incerteza fazendo `medida.nominal(unidade)` ou `medida.incerteza(unidade)`,
repare que é necessário especificar uma unidade, visto que o valor nominal/incerteza são totalmente dependentes
dela. É importante notar que somente em casos bem específicos você vai acessar diretamente esses valores, se você usa muito essas funções talvez não esteja usando corretamente a biblioteca

```py title="Cálculo de IMC"
--8<-- "tests/test_doc_imc.py:9:10"
```

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

O critério usado é da apostila:

- EQUIVALENTES: \(|\Delta \mu| \le 2(\sigma_1+\sigma_2)\)
- INCONCLUSIVO: \(2(\sigma_1+\sigma_2) < |\Delta \mu| < 3(\sigma_1+\sigma_2)\)
- DIFERENTES: \(|\Delta \mu| \ge 3(\sigma_1+\sigma_2)\)

Intuitivamente, a comparação é feita pelo quanto os valores nominais são diferentes e quanta incerteza temos nas medidas.

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