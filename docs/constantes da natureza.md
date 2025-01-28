Muitas constantes da natureza são usadas para cálculos físicos. Alguns exemplos são \(\pi\), \(c\) e \(G\). A biblioteca possui um submódulo chamado **constantes** que armazena esses valores segundo a [CODATA2022](https://arxiv.org/abs/2409.03787). É altamente recomendado que você utilize um editor de texto com **autocompletar** para rapidamente encontrar a constante desejada.

## Exatas
Como os nomes das constantes são geralmente verbosos, é interessante salvar a constante com uma variável de nome reduzido no seu código. O código abaixo calcula o tempo que um fóton leva para sair do Sol e chegar até a Terra, usando a velocidade da luz e o semi-eixo maior médio da órbita da Terra:

```py
--8<-- "tests/test_doc_constantes.py:2:9"
```

Repare como não há incerteza no resultado anterior. Isso porque a velocidade da luz e a unidade astronômica são **exatas**. A velocidade da luz, por exemplo, é usada para a própria definição de distância no sistema métrico. O único erro vem da precisão finita de floats, geralmente na casa de \(~10^{-16}\) no caso do [Python](https://docs.python.org/3/library/sys.html#sys.float_info).

**Uma medida com incerteza nula se comporta como uma medida comum.**

## Inexatas
As constantes do exemplo anterior eram exatas porque eram definições do sistema métrico. No próximo exemplo, do cálculo do campo magnético de um solenoide, será usada a constante de permeabilidade magnética \(\mu_0\) = (1,2566370613 ± 2E-10)x10⁻⁶ N/A², que possui uma pequena incerteza:

```py
--8<-- "tests/test_doc_constantes_com_incerteza.py:4:8"
```