from LabIFSC2 import *


def test_doc_regressoes_construir():
    

    tempos=linspaceM(0,5,10,'s',0.01)
    alturas=arrayM([0,1.4,6,13,24,36,52,70,95,120],'m',0.1)
    #y=y0 + vt + 1/2gt²
    parabola=regressao_polinomial(tempos,alturas,2)
    
    print(parabola)
    a=parabola.a
    b=parabola.b
    c=parabola.c
    print(f"gravidade {a*2}")
    print(f"velocidade inicial {b:E0}")
    print(f"altura inicial {c:E0}")

    assert str(2*a)=="(9,9 ± 0,3) m/s²"
    assert f"{b:E0}"=="(-0,8 ± 0,7) m/s"
    assert f"{c:E0}"=="(0,4 ± 0,7) m"

    tempos=linspaceM(0,10,11,'year',0)
    massa=arrayM([1, 4.7e-1 , 2.3e-1 , 1.2e-1 ,
                6.23e-2, 3.11e-2 ,1.53e-2 ,7.8e-3 ,
                4e-3 ,2e-3 ,1e-3],'kg',0)
    exponencial=regressao_exponencial(tempos,massa,base=2)
    print(exponencial)
    M_0=exponencial.amplitude
    meia_vida=-1/exponencial.expoente
    print(f"{M_0:E0}")
    print(f"{meia_vida:a_E0}")

    assert f"{M_0:E0}"=="(0,95 ± 0,01) kg"
    assert f"{meia_vida:a_E0}"=="(1,011 ± 0,004) a"