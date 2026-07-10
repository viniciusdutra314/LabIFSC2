import pytest

import LabIFSC2 as lab


def test_inicializacao():
    with pytest.raises(ValueError):
        lab.Medida(5, '', -1)
    try:
        lab.Medida(5, 'mm', 0.1)
        lab.Medida(5, 'mm')
        lab.Medida(5, 'mm',0)
    except Exception as exc:
        assert False, "Não deveria levantar um erro"


def test_gt_ge_lt_le():
    x = lab.Medida(5, 'm', 0.1)
    y = lab.Medida(5, 'm', 0.1)
    assert not (x > y)
    assert x >= y
    assert x <= y
    assert not (x > x)
    assert not (x < x)
    assert x >= x
    assert x <= x
    
    z = lab.Medida(6, 'm', 0.1)
    assert z > x
    assert not (x > z)
    assert x < z
    assert (x <= z)
    assert not(x >= z)


def test_comparacoes():
    x=lab.Medida(5, '', 1)
    y=lab.Medida(6, '', 0.1)
    comparacoes=[lambda x,y: x==y,lambda x,y: x!=y]
    for comparacao in comparacoes:
        with pytest.raises(TypeError):
            comparacao(x,y)
    comparacoes=[lambda x,y: x<y,lambda x,y: x<=y,lambda x,y: x>y,lambda x,y: x>=y]
    for comparacao in comparacoes:
        with pytest.raises(TypeError):
            comparacao(x,3)


def test_igualdades():
    x=lab.Medida(1, '', 0.1)
    y=lab.Medida(0.9, '', 0.01)
    z=lab.Medida(50, '', 1)
    w=lab.Medida(45, '', 1)
    assert lab.comparar_medidas(x,y)==lab.Comparacao.EQUIVALENTES
    assert lab.comparar_medidas(x,z)==lab.Comparacao.DIFERENTES
    assert lab.comparar_medidas(z,w)==lab.Comparacao.INCONCLUSIVO

    assert lab.comparar_medidas(x,y,sigma_inferior=0.1,sigma_superior=0.2)==lab.Comparacao.DIFERENTES
    assert lab.comparar_medidas(x,z,sigma_inferior=100,sigma_superior=105)==lab.Comparacao.EQUIVALENTES

    with pytest.raises(ValueError):
        lab.comparar_medidas(x,y,sigma_inferior=5,sigma_superior=1) 
        