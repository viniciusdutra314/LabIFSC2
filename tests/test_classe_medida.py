import pytest

import LabIFSC2 as lab


def test_inicializacao():
    with pytest.raises(ValueError):
        lab.Medida(5,-1,'')
    inicializacoes_erradas=[lambda: lab.Medida("1",3,''),
                            lambda: lab.Medida(5,"0.1",''),
                            lambda: lab.Medida([],3,'mm')]
    for inicializacao_errada in inicializacoes_erradas:
        with pytest.raises(TypeError):
            inicializacao_errada()
    try:
        lab.Medida(5,0.1,'mm')
    except Exception as exc:
        assert False, "Não deveria levantar um erro"

def test_valores_protegidos(): 
    x=lab.Medida(10,1,'')
    with pytest.raises(PermissionError):
        x.incerteza=3
    with pytest.raises(PermissionError):
        del x.incerteza
    with pytest.raises(PermissionError):
        x.nominal=1
    with pytest.raises(PermissionError):
        del x.nominal
    with pytest.raises(PermissionError):
        x.unidade='mm'
    with pytest.raises(PermissionError):
        del x.unidade
    with pytest.raises(PermissionError):
        x.histograma='mm'
    with pytest.raises(PermissionError):
        del x.histograma

def test_comparacoes():
    x=lab.Medida(5,1,'')
    y=lab.Medida(6,0.1,'')
    comparacoes=[lambda x,y: x==y,lambda x,y: x!=y,
                 lambda x,y: x>y, lambda x,y: x>=y,
                 lambda x,y: x<y, lambda x,y: x<=y]
    for comparacao in comparacoes:
        with pytest.raises(TypeError):
            comparacao(x,y)
    
def test_igualdades():
    x=lab.Medida(1,0.1,'')
    y=lab.Medida(0.9,0.01,'')
    z=lab.Medida(50,1,'')
    w=lab.Medida(45,1,'')
    assert lab.comparar_medidas(x,y)==lab.Comparacao.EQUIVALENTES
    assert lab.comparar_medidas(x,z)==lab.Comparacao.DIFERENTES
    assert lab.comparar_medidas(z,w)==lab.Comparacao.INCONCLUSIVO

    assert lab.comparar_medidas(x,y,sigma_inferior=0.1,sigma_superior=0.2)==lab.Comparacao.DIFERENTES
    assert lab.comparar_medidas(x,z,sigma_inferior=100,sigma_superior=105)==lab.Comparacao.EQUIVALENTES

    with pytest.raises(ValueError):
        lab.comparar_medidas(x,y,sigma_inferior=5,sigma_superior=1) 