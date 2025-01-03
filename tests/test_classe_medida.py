import LabIFSC2 as lab
import pytest

def test_eq_operator():
    x=lab.Medida(5,1)
    y=lab.Medida(6,0.1)
    comparacoes=[lambda x,y: x==y,lambda x,y: x!=y,
                 lambda x,y: x>y, lambda x,y: x>=y,
                 lambda x,y: x<y, lambda x,y: x<=y]
    for comparacao in comparacoes:
        with pytest.raises(TypeError):
            comparacao(x,y)
    
    