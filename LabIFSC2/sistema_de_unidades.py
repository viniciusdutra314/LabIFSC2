import re
from fractions import Fraction

import numpy as np

TODAS_UNIDADES={}

class Unidade:
    def __init__(self,nome:str,simbolo:str,latex:str,dimensao:list,
                 cte_mult:float =1,cte_ad :float =0,registar=True):
        ''' Classe criada para armazenar e registar unidades, todas as
        informações relacionadas a nome,simbolo,latex, dimensão e as constantes
        usadas para converter a unidade para o SI, são guardadas aqui
        Para criar uma unidade nova bastar entrar nesse arquivo (unidades.py) 
        e criar uma instância nova de Unidade, exemplo
 
        Unidade("unidade astronômica","ua","ua",[0,1,0,0,0,0,0],"1.495978707e11")

        Convenção da ordem da Dimensão
        Dimensão=[T,L,M,I,Θ,N,J]
        T=tempo ,L=comprimento ,M=massa
        I=corrente, Θ=Temperatura , N=mol , J=cd
        '''
        self.nome=nome ; self.simbolo=simbolo
        self.latex=latex ; self.dimensao=np.array(dimensao)
        self.cte_ad=cte_ad ; self.cte_mult=cte_mult
        if registar:
            global TODAS_UNIDADES
            TODAS_UNIDADES[simbolo]=self
    def __repr__(self) -> str:
        return f'Unidade({self.nome=}, {self.simbolo=}, {self.latex=}, {self.dimensao=},{self.cte_mult=},{self.cte_ad=})'

def separar_unidades(texto :str) -> tuple[list[str],list[Fraction]]:
    """
    Examples:
    >>> separar_unidades('kg m')
    (['kg', 'm'], [Fraction(1, 1), Fraction(1, 1)])
    >>> (['kg', 'm', 's'], [Fraction(1, 1), Fraction(1, 1), Fraction(-2, 1)])
    (['kg', 'm', 's'], [Fraction(1, 1), Fraction(1, 1), Fraction(-2, 1)])
    >>> separar_unidades('degC m1/2 s-3/2 kg1')
    (['degC', 'm', 's', 'kg'], [Fraction(1, 1), Fraction(1, 2), Fraction(-3, 2), Fraction(1, 1)])
    """
    unidades_com_expoentes=texto.split()
    unidades=[] ; expoentes=[]
    for unidade_com_expoente in unidades_com_expoentes:
        match_expoente = re.search(r'[-]?\d+[/]?\d*', unidade_com_expoente) 
        if not match_expoente:
            expoentes.append(Fraction(1))
            unidades.append(unidade_com_expoente)
        else:
            index=match_expoente.start()
            expoente=Fraction(unidade_com_expoente[index:])
            unidade=unidade_com_expoente[:index]
            expoentes.append(expoente)
            unidades.append(unidade)
    return unidades, expoentes


def multiplicar_unidades(texto_inteiro : str, unidades_str : list[str],
                        expoentes : list[Fraction], TODAS_UNIDADES):
    unidades=[TODAS_UNIDADES[x] for x in unidades_str]
    cte_mult=1 ; cte_ad=0 ; dimensao=np.zeros(7)
    for unidade,expoente in zip(unidades,expoentes):
        cte_mult*=unidade.cte_mult**expoente
        dimensao+=unidade.dimensao
    
    
    return Unidade(nome='não definido',simbolo=texto_inteiro,
                   latex=texto_inteiro,dimensao=dimensao,
                   cte_mult=cte_mult,cte_ad=0)