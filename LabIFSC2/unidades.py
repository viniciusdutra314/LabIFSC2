import numpy as np
TODAS_UNIDADES={}
class Unidade:
    def __init__(self,nome:str,simbolo:str,latex:str,dimensao:list,
                 cte_mult:float =1,cte_ad :float =0):
        ''' Classe criada para armazenar e registar unidades, todas as

        informações relacionadas a nome,simbolo,latex, dimensão e as constantes

        usadas para converter a unidade para o SI, são guardadas aqui

        Para criar uma unidade nova bastar entrar nesse arquivo

        (unidades.py) e criar uma instância nova de Unidade, exemplo

        Unidade("unidade astronômica","ua","ua",[0,1,0,0,0,0,0],"1.495978707e11")

        Convenção da ordem da Dimensão
        Dimensão=[T,L,M,I,Θ,N,J]
        
        T=tempo

        L=comprimento
        
        M=massa

        I=corrente

        Θ=Temperatura

        N=mol

        J=cd
        '''
        self.nome=nome ; self.simbolo=simbolo
        self.latex=latex ; self.dimensao=np.array(dimensao)
        self.cte_ad=cte_ad ; self.cte_mult=cte_mult
        global TODAS_UNIDADES
        TODAS_UNIDADES[simbolo]=self
Unidade("adimensional","adimensional","",[0,0,0,0,0,0,0])
Unidade("Newton","N","N",[-2,1,1,0,0,0,0])
Unidade("Dina","Dyn","Dyn",[-2,1,1,0,0,0,0],1e-5)

#distância padrão
Unidade("metro","m","m",[0,1,0,0,0,0,0])
Unidade("centimetro","cm","cm",[0,1,0,0,0,0,0],1e-2)
Unidade("milimetro","mm","mm",[0,1,0,0,0,0,0],1e-3)
Unidade("micrometro","um","μm",[0,1,0,0,0,0,0],1e-6)
Unidade("micrometro","μm","μm",[0,1,0,0,0,0,0],1e-6)
Unidade("nanometro","nm","nm",[0,1,0,0,0,0,0],1e-9)
#distância astronomia