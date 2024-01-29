Não é necessário ser um desenvolvedor para contribuir com o projeto, 
caso tenha encontrado algum **bug** ou tenha alguma **sugestão**
abra uma [issue](https://github.com/viniciusdutra314/LabIFSC2/issues) no repositório do projeto, algumas pequenas contribuições são possíveis com pouco conhecimento
técnico em [Nova Unidade](#nova-unidade) e [Nova Constante](#nova-constante).

Caso seja um desenvolvedor e queira contribuir com algo mais profundo acesse
a parte da documentação sobre [Ambiente de desenvolvimento](#ambiente-de-desenvolvimento) e [Possíveis contribuições](#possíveis-contribuições)

## Nova unidade
A quantidade de unidades usadas no mundo é enorme, talvez alguma unidade mais específica
que você venha precisar não exista na biblioteca, basta criar um fork da biblioteca,
adicionar a unidade na pasta LabIFSC2/unidades.py através da classe Unidade e enviar
um pull request

```{.py3 title='Exemplo de unidade'}
        #nome #       simbolo #latex #dimensão  #conversão multiplicativa para si
Unidade("Carga elementar","e","e",[1,0,0,1,0,0,0],1.602176634e-19)
#Dimensão=[T,L,M,I,Θ,N,J] 
#T=tempo L=comprimento M=massa
#I=corrente Θ=Temperatura N=mol J=cd
```
Caso queira adicionar uma unidade estranha que necessite de uma multiplicação e soma
para converter para o si (um exemplo seria o **Fahrenheit**), basta preencher o último espaço com uma constante aditiva
```{.py3 title='Unidade mais complexa'}
            #nome        #simbolo #latex     #dimensão  #cte mul #cte aditiva
    Unidade("Fahrenheit", "ºF", r"^\circ F",[0,0,0,0,1,0,0],5/9,255.372)
```
## Nova constante
A mesma vastidão de unidades também ocorre com constantes da natureza, para 
adicionar uma nova basta ir em LabIFSC2/constantes/constantes.py e adicionar sua constante,
coloque o maior número de casas decimais que puder e também a incerteza associada
a essa constante se houver. Sinta-se livre para adicionar constantes matemáticas 
como \(\phi\) e até mesmo \(\gamma\)
## Nova formatação
Atualmente só existem 2 [formatações](LaTeX/Notação%20científica.md) disponíveis, caso
queira adicionar uma nova será necessário mudar a função *__format__* da classe Medida e adicionar um novo condicional do parâmetro fmt, algumas funções convenientes estão
no arquivo *formatacoes.py*

## Ambiente de desenvolvimento
Para o gerenciamento de dependências foi escolhido o [Poetry](https://python-poetry.org/), mesmo que só o Numpy seja uma dependência de uso, existem várias dependências
de desenvolvimento, para instalar elas basta usar alguns comandos com o poetry
```{bash title='Clonar o repositório'}
git clone https://github.com/viniciusdutra314/LabIFSC2
```
```{bash title='Instalar ambiente virtual'}
poetry install && poetry shell
```
Várias tarefas foram automatizadas com o [Taskipy](https://github.com/taskipy/taskipy), então para rodar os testes com o [Pytest](https://docs.pytest.org/) basta digitar o comando abaixo, é importante lembrar que esse comando também executa teste
de formatação de código com o [Isort](https://pycqa.github.io/isort/) e [Blue](https://blue.readthedocs.io/en/latest/), então tome cuidado para não escrever códigos que fogem da formatação do projeto
```{bash title='Rodar testes'}
task testes
```
Para montar a documentação localmente no seu computador basta usar o task docs que
é um alias para o comando em [Mkdocs](https://www.mkdocs.org/) mkdocs serve

```{bash title='Montar documentação'}
task docs
```
## Possíveis contribuições
1) Nem sempre as variáveis que medimos são gaussianas, a criação de novas classes
além da Medida como Poisson, Uniforme,Binominal talvez seja uma boa ideia, eu 
implementaria como uma classe abstrata e estenderia a função montecarlo para receber
objetos dessa classe, mas isso é só uma sugestão

2) 