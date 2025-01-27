from LabIFSC2 import *


def test_doc_lei_de_hook():
    import matplotlib.pyplot as plt

    

    forças=linspaceM(0,10,10,'N',0.1) #variando a força
    deslocamentos=arrayM([0,0.5,1.1,1.6,2,2.3,2.8,3.2,3.7,4],'cm',0.01) #medindo deslocamentos

    reta=regressao_linear(deslocamentos,forças)
    print(reta)
    #MPolinomio(coefs=[(2,51 ± 0,06) N/cm, (-3 ± 2)x10⁻¹ N],grau=1)
    print(f"Constante da mola {reta.a:si}") 
    #Constante da mola (2,51 ± 0,06)x10² kg/s²

    unidade_x='cm'
    unidade_y='N'

    plt.style.use('ggplot')

    plt.scatter(nominais(deslocamentos,unidade_x),
            nominais(forças,unidade_y),
            label='Dados',
            color='red')

    x=linspaceM(0,4,100,unidade_x,0)

    plt.plot(nominais(x,unidade_x),
            reta.amostrar(x,unidade_y),
            label='Regressão linear',
            color='blue')

    plt.xlabel(f'Deslocamento ({unidade_x})')
    plt.ylabel(f'Força ({unidade_y})')