## Não use listas, use np.array
Um erro comum que eu vejo em iniciantes em Python é o uso excessivo de listas, para resumir o que poderia ser uma longa aula de estruturas de dados, para que listas possam ter elementos de diferentes tipos e comprimento dinâmico, essa flexibilidade causa perda de performance, só use listas se você realmente precise desses comportamentos, de forma geral, listas não devem ser usadas para representar vetores/matrizes, a estrutura mais eficiente em termos de memória/processamento são **arrays**.

Mesmo que a própria linguagem python tenha um módulo de [arrays](https://docs.python.org/pt-br/3.13/library/array.html), historicamente a implementação mais usada é a do Numpy, **o uso de arrays numpy é obrigatório no LabIFSC2, usar listas simplesmente retorna erro**. Eu tomei essa decisão para que os alunos de graduação adquiriam familiaridade com talvez a mais importante biblioteca científica do python, o numpy 

## Operações elementares