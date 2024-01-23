from LabIFSC2 import *
import pytest
def test_distancias():
    x=Medida(5.32,0.2,"m")
    assert str(x.converte("cm")) == "(5.3 ± 0.2)E2 cm"
    assert str(x.converte("mm")) == "(5.3 ± 0.2)E3 mm"
    assert str(x.converte("um")) == "(5.3 ± 0.2)E6 um"
    assert str(x.converte("nm")) == "(5.3 ± 0.2)E9 nm"
def test_igualdade_unidades_diferentes():
  statements=[lambda : Medida(5.32,0.2,"m")==Medida(135,0,"N"),
              lambda : Medida(5.32,0.2,"m")>Medida(135,0,"N"),
              lambda : Medida(5.32,0.2,"m")>=Medida(135,0,"N"),
              lambda : Medida(5.32,0.2,"m")<=Medida(135,0,"N"),
              lambda : Medida(5.32,0.2,"m")<Medida(135,0,"N"),
              lambda : Medida(5.32,0.2,"m")!=Medida(135,0,"N")] 
  for index, statement in enumerate(statements):
    with pytest.raises(ValueError):
     statement()
def test_igualdade_unidades_iguais():
    x=Medida(5,0.3)
    y=Medida(136,53)
    assert x>=4 
    assert x<10
    assert y>x
    assert x<y
    z=Medida(6,0.3,"m")
    w=Medida(136,0.2,"cm")
    assert z>w
    print(w)