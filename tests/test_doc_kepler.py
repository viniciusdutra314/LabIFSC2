import matplotlib.pyplot as plt
import numpy as np

import LabIFSC2 as lab
from LabIFSC2 import *


def test_doc_kepler():
    #https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_british.html
    dados = [
        {"planeta": "Mercúrio", "distancia_em_milhoes_milhas": 36.0, "orbita_em_dias": 88.0},
        {"planeta": "Vênus", "distancia_em_milhoes_milhas": 67.2, "orbita_em_dias": 224.7},
        {"planeta": "Terra", "distancia_em_milhoes_milhas": 93.0, "orbita_em_dias": 365.2},
        {"planeta": "Marte", "distancia_em_milhoes_milhas": 141.6, "orbita_em_dias": 687.0},
        {"planeta": "Júpiter", "distancia_em_milhoes_milhas": 483.7, "orbita_em_dias": 4331.0},
        {"planeta": "Saturno", "distancia_em_milhoes_milhas": 889.8, "orbita_em_dias": 10747.0},
        {"planeta": "Urano", "distancia_em_milhoes_milhas": 1781.5, "orbita_em_dias": 30589.0},
        {"planeta": "Netuno", "distancia_em_milhoes_milhas": 2805.5, "orbita_em_dias": 59800.0},
    ]
    distancias=np.array([Medida(planeta["distancia_em_milhoes_milhas"],"Mmiles",0) for planeta in dados])
    periodos=np.array([Medida(planeta["orbita_em_dias"],"days",0) for planeta in dados])
    fitting=regressao_potencia(distancias,periodos)
    
    print(f"{fitting.potencia}")#(1,4979 ± 0,0008)
    G=constantes.Newtonian_constant_of_gravitation
    pi=constantes.pi
    massa_sol=constantes.solar_mass
    constante_teorica=np.sqrt(4*pi**2/(G*massa_sol))
    print(f"Teórica:{constante_teorica:si}") #(5,4540 ± 0,0001)x10⁻¹⁰ s/m¹⋅⁵
    print(f"Experimental:{fitting.cte_multiplicativa:si}") #(5,59 ± 0,03)x10⁻¹ s/m¹⋅⁴⁹⁷⁸⁷

    assert f"{fitting.potencia}"=="(1,4979 ± 0,0008) "
    assert f"{constante_teorica:si}"=="(5,4540 ± 0,0001)x10⁻¹⁰ s/m¹⋅⁵"
    assert f"{fitting.cte_multiplicativa:si}"=="(5,76 ± 0,03)x10⁻¹⁰ s/m¹⋅⁴⁹⁷⁸⁷"

    unidade_x='astronomical_unit'
    unidade_y='years'

    x=linspaceM(0,30,100,'astronomical_unit',0)
    amostragem=fitting.amostrar(x,unidade_y)
    print(amostragem)
    '''
    [  0.           0.16720236   0.47222204   0.86677871   1.33367488
    1.86297947   2.44799678   3.08382118   3.76665199   4.49338729
    5.26151605   6.06894605   6.91380503   7.7943936    8.70950132
    9.6576868   10.637894    11.64919283  12.6904141   13.76086203
    14.85993445  15.98652     17.14022277  18.32023888  19.5262253
    20.7574556   22.01355905  23.29377595  24.59812236  25.92529963
    27.27589755  28.64912586  30.04414761  31.46106333  32.90057751
    34.35997688  35.84108923  37.34286772  38.8647287   40.40618418
    41.96774186  43.54918181  45.1495475   46.77017268  48.40808983
    50.06563503  51.74134587  53.43456287  55.14656257  56.8772764
    58.62478682  60.38904278  62.17100623  63.97154288  65.78745354
    67.62110684  69.47029197  71.3363668   73.22010168  75.11830551
    77.03396015  78.96476666  80.91117912  82.87311834  84.85279027
    86.84630189  88.85517283  90.88003283  92.91871024  94.97238155
    97.04086489  99.12494062 101.22470506 103.33573288 105.46558935
    107.60652663 109.76323664 111.93360799 114.1169974  116.31588584
    118.5287959  120.75651541 122.99423608 125.24817432 127.51591977
    129.79705056 132.08950466 134.39633912 136.71555037 139.05241296
    141.39816295 143.75757548 146.13123689 148.51706457 150.91355481
    153.32539889 155.74978066 158.18744411 160.63534066 163.09497686]
    '''
    
    plt.style.use('ggplot')
    plt.plot(nominais(x,unidade_x),
             amostragem,
             color='red',
             label='Teórica')
    plt.scatter(
            nominais(distancias,unidade_x),
            nominais(periodos,unidade_y),
            color='blue',
            label='Dados')
    plt.xlabel(f'Distâncias ({unidade_x})')
    plt.ylabel(f'Períodos ({unidade_y})')
    plt.legend()
    plt.savefig('docs/images/kepler.jpg',dpi=300)
    plt.cla()


    print(curva_min(fitting,'years')[0:5])
    #[0 0.16563505 0.46786682 0.85881466 1.3214152 ]
    print(curva_max(fitting,'years')[0:5])
    #[0  0.16875531 0.47653809 0.87467204 1.34582704]
