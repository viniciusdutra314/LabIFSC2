## Não use listas, use np.array
Um erro comum que eu vejo em iniciantes em Python é o uso excessivo de listas, para resumir o que poderia ser uma longa aula de estruturas de dados, para que listas possam ter elementos de diferentes tipos e comprimento dinâmico, essa flexibilidade causa perda de performance, só use listas se você realmente precise desses comportamentos, de forma geral, listas não devem ser usadas para representar vetores/matrizes, a estrutura mais eficiente em termos de memória/processamento são **arrays**.

Mesmo que a própria linguagem python tenha um módulo de [arrays](https://docs.python.org/pt-br/3.13/library/array.html), historicamente a implementação mais usada é a do Numpy, **o uso de arrays numpy é obrigatório no LabIFSC2, usar listas simplesmente retorna erros**. Eu tomei essa decisão para que os alunos de graduação adquiriam familiaridade com talvez a mais importante biblioteca científica do python, o numpy 

## Operações elementares

Com arrays numpy temos a magia da vetorização, ou seja, podemos fazer operações matemáticas
entre arrays, o resultado disso são operações elemento a elemento

```py
--8<-- "tests/test_doc_operacoes_basicas_arrays.py:5:14"
```

## Operações matemáticas
Como discutido na secção de [Funçõs matemáticas](funcoes_matematicas.md), as funções do numpy podem atuar diretamente na classe Medida.

```py 
--8<-- "tests/test_doc_sqrt_vetorizado.py:5:10"
```

## linspaceM
Em muitas medidas experimentais nós fazemos medições igualmente espaçadas, imagine que 
você está medindo o campo magnético de um fio em função da sua distância \(\vec{B}(distância)\),
você realiza uma medição a cada 1cm por exemplo, o lab.linspace recebe o valor da primeira medição,
o valor da última, a quantidade de medições entre elas, a incerteza da medição e a unidade.
No exemplo abaixo nós fizemos 10 medições entre [1cm,10cm], com precisão de 0.05cm cada

```py 
--8<-- "tests/test_doc_linspace.py:5:9"
```

A função é o análogo do [np.linspace](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html#numpy-linspace) que recebe medidas

##

## arrayM
Agora que temos as distâncias nós medimos o campo magnético pra cada distância, como registramos esses campos?
teríamos que criar 10 objetos `Medida` diretamente? Não, a solução é o lab.arrayM, ele recebe uma lista/array
de valores nominais, a incerteza das medidas e a unidade 
```py 
--8<-- "tests/test_doc_linspace.py:10:13"
```