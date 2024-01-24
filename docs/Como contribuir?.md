Não é necessário ser um desenvolvedor para contribuir com o projeto, 
caso tenha encontrado algum **bug** ou tenha alguma **sugestão**
abra uma [issue](https://github.com/viniciusdutra314/LabIFSC2/issues) no repositório do projeto

## Nova unidade
A quantidade de unidades usadas no mundo é enorme, talvez alguma unidade mais específica
que você venha precisar não exista na biblioteca, basta criar um fork da biblioteca,
adicionar a unidade na pasta LabIFSC2/unidades.py através da classe Unidade e enviar
um pull request

```{.py3 title='Exemplo de unidade'}
        #nome #       simbolo #latex #dimensão  #conversão multiplicativa para si
Unidade("Carga elementar","e","e",[1,0,0,1,0,0,0],1.602176634e-19)
#Dimensão=[T,L,M,I,Θ,N,J] 
#T=tempo
#L=comprimento
#M=massa
#I=corrente
#Θ=Temperatura
#N=mol
#J=cd
```
Caso queira adicionar uma unidade estranha que necessite de uma multiplicação e soma
para converter para o si (um exemplo seria o **Fahrenheit**), basta preencher o último
espaço com uma constante multiplicativa
```{.py3 title='Unidade mais complexa'}
            #nome        #simbolo #latex     #dimensão  #cte mul #cte aditiva
    Unidade("Fahrenheit", "ºF", r"^\circ F",[0,0,0,0,1,0,0],5/9,255.372)
```
## Nova constante
A mesma vastidão de unidades também ocorre com constantes da natureza, para 
adicionar uma nova basta ir em LabIFSC2/constantes.py e adicionar sua constante,
coloque o maior número de casas decimais que puder e também a incerteza associada
a essa constante se houver. Sinta-se livre para adicionar constantes matemáticas 
como \(\phi\) e até mesmo \(\gamma\)

```{.py3 title='Exemplo de constante exata'}
                  #nominal #
    C_SPEED=Medida(299792458,0,'m/s')
```


## Possíveis contribuições
1) Nem sempre as variáveis que medimos são gaussianas, a criação de novas classes
além da Medida como Poisson, Uniforme,Binominal talvez seja uma boa ideia, eu 
implementaria como uma classe abstrata e estenderia a função montecarlo para receber
objetos dessa classe, mas isso é só uma sugestão

2) 