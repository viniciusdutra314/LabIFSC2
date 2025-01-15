Muitas constantes da natureza são usadas para cálculos físicos. Alguns exemplos são \(\pi\), \(c\) e \(G\). A biblioteca possui um submódulo chamado **constantes** que armazena esses valores segundo a [CODATA2022](https://arxiv.org/abs/2409.03787). É altamente recomendado que você utilize um editor de texto com **autocompletar** para rapidamente encontrar a constante desejada.

<img src=autocomplete.png alt='Exemplo com autocomplete' width=500>

## Exemplos

Como os nomes das constantes são geralmente verbosos, é interessante salvar a constante com uma variável de nome reduzido no seu código. O código abaixo calcula o tempo que um fóton leva para sair do Sol e chegar até a Terra, usando a velocidade da luz e o semi-eixo maior médio da órbita da Terra:


```python
--8<-- "docs/Constantes/codigo_exemplo.py:7:12"
```


As constantes do exemplo anterior eram exatas porque eram definições do sistema métrico. No próximo exemplo, será usada a constante de permeabilidade magnética \(\mu_0\) = (1.25663706212 ± 0.00000000000019)E-6 N A^-2, que possui uma pequena incerteza. Todas as constantes são tratadas como Medidas, mesmo as que são exatas:

```{.py3 title='Campo magnético de um solenoide infinito'}
import LabIFSC2 as lab
mu_0 = lab.constantes.vacuum_mag_permeability
N = 100
L = lab.Medida(30, 0.1, 'm')
I = lab.Medida(200, 0.1, 'mA')
B = mu_0 * N * I / L
```
