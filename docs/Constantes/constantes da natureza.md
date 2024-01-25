Muitas constantes da natureza são usadas para cálculos físicos, alguns
exemplos são \(\pi\), \(c\) , \(G\). A biblioteca possui um submódulo
chamado **constantes** que armazena esses valores segundo a [CODATA2018](https://www.nist.gov/publications/codata-recommended-values-fundamental-physical-constants-2018), é altamente recomendado que você utilize um editor de texto com **autocomplete** de forma
a rapidamente encontrar a constante desejada
<img src=autocomplete.png alt='Exemplo com autocomplete' width=500>
##Exemplos
Como os nomes das constantes são geralmente verbosos é interessante
salvar a constante com uma varíavel de nome reduzido no seu código, o código abaixo
calcula o tempo de um fóton sair do Sol e chegar até a Terra usando assim a velocidade da luz e o semi-eixo maior médio da órbita da Terra
```{.py3 title='Velocidade da causalidade'}
import LabIFSC2 as lab
UA=lab.constantes.astronomical_unit
c=lab.constantes.speed_of_light_in_vacuum
tempo=UA/c #(4.9900478383615643)E2 s
#8 min 19s
``` 
As constantes do exemplo anterior eram exatas porque eram
definições do sistema métrico, já no próximo exemplo será
usada a constante de permeabilidade magnetica \(\mu\)=(1.25663706212 ± 00000000000019)E-6 N A^-2 ela possui uma pequena incerteza, todas as constantes
são tratadas como Medidas mesmo as que são exatas 
```{.py3 title='Campo magnético de um solenoide infinito'}
import LabIFSC2 as lab
mu_0=lab.constantes.vacuum_mag_permeability
N=100
L=lab.Medida(30,0.1,'m')
I=lab.Medida(200,0.1,'mA')
B=mu_0*N*I/L
```