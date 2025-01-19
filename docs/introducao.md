A grande classe da biblioteca é a `Medida`, ela recebe 3 argumentos para sua inicialização

- Nominal (\(\mu\)) : Valor medido ou média dos valores medidos 

- Incerteza (\(\sigma\)): Incerteza experimental ou dispersão das medidas 

- Unidade: Unidade da medida (precisa ser a mesma do valor nominal e incerteza)

Para um exemplo prático consideraremos um tipo de medida comum, o IMC (não confundir com ICMC). Suponhamos que uma pessoa foi medida (valores fictícios) com uma fita métrica e temos somente certeza na casa de 1cm e usamos uma balança com precisão de 100g. 

Com o LabIFSC2 podemos fazer os cálculos assim:

```py title="Cálculo de IMC"
--8<-- "tests/test_doc_imc.py:1:6"
```
Calculamos então que o IMC tem valor esperado de \(\mu=24,5\) e desvio padrão de \(\sigma=0.3\), ok mas o que isso significa?

### Intervalo de confiança
Como estamos falando de medidas experimentais, falamos de **intervalos** e não valores exatos. Objetos da classe `Medida` possuem um método chamado `intervalo_de_confiança`, com ele podemos 
especificar uma probabilidade `p` de estarmos representando os valores possíveis das Medidas

```py title="Intervalo de confiança IMC"
--8<-- "tests/test_doc_imc.py:7:8"
```
Basicamente isso significa que estamos 95% certos que o IMC está entre \(23,95\le IMC \le 25.05\). Talvez você esteja surpreso que pelo método de medida temos 1 unidade inteira de IMC podendo variar


### Comparando Medidas
Se uma segunda pessoa afirmar que seu IMC é de (25 ± 0.1), podemos dizer que seus IMC são equivalentes? Mesmo que \(25 \ne 24.5\), pela incerteza nas medidas podemos dizer que essa diferença está na margem de erro do experimento. 

O método que faz essa comparação é comparar_medidas que recebe duas Medidas e retorna se elas são:

- EQUIVALENTES 
- DIFERENTES 
- INCONCLUSIVO 

```py title="Comparando IMC"
--8<-- "tests/test_doc_equivalencia.py:1:6"
```
