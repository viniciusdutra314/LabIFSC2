## Não use listas, use np.array

Um erro comum que vejo em iniciantes em Python é o uso excessivo de listas. Para resumir o que poderia ser uma longa aula de estruturas de dados, listas podem ter elementos de diferentes tipos e comprimento dinâmico. Essa flexibilidade causa perda de performance. Só use listas se você realmente precisar desses comportamentos. De forma geral, listas não devem ser usadas para representar vetores/matrizes. Nesse caso a estrutura mais eficiente em termos de memória e processamento são **arrays**.

Mesmo que a própria linguagem Python tenha um módulo de [arrays](https://docs.python.org/pt-br/3.13/library/array.html), historicamente a implementação mais usada é a do Numpy. **O uso de arrays numpy é obrigatório no LabIFSC2, usar listas simplesmente retorna erros**[^1]. Eu tomei essa decisão para que os alunos de graduação adquiram familiaridade com talvez a mais importante biblioteca científica do Python, o Numpy.

## Operações elementares

Com arrays numpy temos a magia da vetorização, ou seja, podemos fazer operações matemáticas entre arrays. O resultado disso são operações elemento a elemento.

```py
--8<-- "tests/test_doc_operacoes_basicas_arrays.py:5:14"
```

Perceba que isso não é possível com listas.
## Operações matemáticas

Como discutido na seção de [Funções matemáticas](funcoes_matematicas.md), as funções do Numpy podem atuar diretamente na classe Medida e em arrays de medidas.

```py 
--8<-- "tests/test_doc_sqrt_vetorizado.py:5:9"
```


## linspaceM

Em muitas medidas experimentais fazemos medições igualmente espaçadas. Imagine que você está medindo o campo magnético de um fio em função da sua distância \(\vec{B}(distância)\). Você realiza uma medição a cada 1 cm, por exemplo. O `lab.linspace` recebe o valor da primeira medição, o valor da última, a quantidade de medições entre elas, a unidade e a incerteza da medição. No exemplo abaixo, fizemos 10 medições entre [1 cm, 10 cm], com precisão de 0,05 cm cada.

```py 
--8<-- "tests/test_doc_linspace.py:5:9"
```

A função é o análogo do [np.linspace](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html#numpy-linspace) que recebe medidas.

## arrayM

Agora que temos as distâncias, medimos o campo magnético para cada distância. Como registramos esses campos? Teríamos que criar 10 objetos `Medida` diretamente? Não, a solução é o lab.arrayM. Ele recebe uma lista/array de valores nominais, a incerteza das medidas e a unidade.

```py 
--8<-- "tests/test_doc_linspace.py:10:13"
```

## Nominais
Para obter os valores nominais de um array numpy de medidas, basta usar a função `nominais(array_medida, unidade)`:
```py
--8<-- "tests/test_doc_nominal.py:7:9"
```

## Incertezas
De maneira análoga, podemos também pegar as incertezas com `incertezas(array_medida, unidade)`:
```py
--8<-- "tests/test_doc_incerteza.py:7:9"
```

[^1]:
    Algumas exceções a essa regra é a criação de uma Medida e o arrayM, que ambos podem receber uma lista. Mas perceba que, no caso do arrayM, a lista está sendo usada diretamente para criar um np.ndarray. Então, na prática, você sempre está lidando com arrays.