from LabIFSC2 import *


def test_doc_regressoes_construir():
    

    tempos=linspaceM(0,5,10,'s',0.01)
    alturas=arrayM([0,1.4,6,13,24,36,52,70,95,120],'m',0.1)
    #y=y0 + vt + 1/2gt²
    parabola=regressao_polinomial(tempos,alturas,2)
    
    print(parabola)#MPolinomio(coefs=[(4,9 ± 0,1) m/s², (-8 ± 7)x10⁻¹ m/s, (4 ± 7)x10⁻¹ m],grau=2)
    a,b,c=parabola
    print(f"gravidade {a*2}") #(9,9 ± 0,3) m/s²
    print(f"velocidade inicial {b:E0}") #(-0,8 ± 0,7) m/s
    print(f"altura inicial {c:E0}") #(0,4 ± 0,7) m

    assert str(parabola)=="MPolinomio(coefs=[(4,9 ± 0,1) m/s², (-8 ± 7)x10⁻¹ m/s, (4 ± 7)x10⁻¹ m],grau=2)"
    assert str(2*a)=="(9,9 ± 0,3) m/s²"
    assert f"{b:E0}"=="(-0,8 ± 0,7) m/s"
    assert f"{c:E0}"=="(0,4 ± 0,7) m"

    tempos=linspaceM(0,10,11,'year',0)
    massa=arrayM([1, 4.7e-1 , 2.3e-1 , 1.2e-1 ,
                6.23e-2, 3.11e-2 ,1.53e-2 ,7.8e-3 ,
                4e-3 ,2e-3 ,1e-3],'kg',0)
    exponencial=regressao_exponencial(tempos,massa,base=2)
    print(exponencial)
    #MExponencial(cte_multiplicativa=(9,3 ± 0,2)x10⁻¹ kg,expoente=(-9,89 ± 0,04)x10⁻¹ 1/a,base=2)
    M_0=exponencial.cte_multiplicativa
    meia_vida=-1/exponencial.expoente
    print(f"{M_0:E0}") #(0,93 ± 0,02) kg
    print(f"{meia_vida:E0}") #(1,011 ± 0,004) a

    assert str(exponencial)=="MExponencial(cte_multiplicativa=(9,3 ± 0,2)x10⁻¹ kg,expoente=(-9,89 ± 0,04)x10⁻¹ 1/a,base=2)"
    assert f"{M_0:E0}"=="(0,93 ± 0,02) kg"
    assert f"{meia_vida:E0}"=="(1,011 ± 0,004) a"