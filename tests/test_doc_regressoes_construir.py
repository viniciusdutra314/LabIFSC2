from LabIFSC2 import *


def test_doc_regressoes_construir():
    

    tempos=linspaceM(0,5,10,'s',0.01)
    alturas=arrayM([0,1.4,6,13,24,36,52,70,95,120],'m',0.1)
    #y=y0 + vt + 1/2gt²
    parabola=regressao_polinomial(tempos,alturas,grau=2)
    a, b, c = parabola # é possível fazer unpacking dos coeficientes
    print(f"gravidade {a*2}") #(9,9 ± 0,3) m/s²
    print(f"velocidade inicial {b:E0}") #(-0,8 ± 0,7) m/s
    print(f"altura inicial {c:E0}") #"0,4 ± 0,7) m
    print(parabola(Medida(10,"s"))) #valor da parabola no tempo 10s 
    assert str(2*a)=="(9,9 ± 0,3) m/s²"
    assert f"{b:E0}"=="(-0,8 ± 0,7) m/s"
    assert f"{c:E0}"=="(0,4 ± 0,7) m"

    tempos=linspaceM(0,10,11,'year',0)
    massa=arrayM([1, 4.7e-1 , 2.3e-1 , 1.2e-1 ,
                6.23e-2, 3.11e-2 ,1.53e-2 ,7.8e-3 ,
                4e-3 ,2e-3 ,1e-3],'kg',0)
    exponencial=regressao_exponencial(tempos,massa,base=2)
    M_0=exponencial.amplitude
    meia_vida=-1/exponencial.expoente
    print(f"{M_0:E0}") #(0,95 ± 0,01) kg
    print(f"{meia_vida:a_E0}") #(1,011 ± 0,004) a
    print(exponencial(Medida(200,"year"))) #massa do material 
                                           #radioativo daqui a 200 anos 
    assert f"{M_0:E0}"=="(0,95 ± 0,01) kg"
    assert f"{meia_vida:a_E0}"=="(1,011 ± 0,004) a"
