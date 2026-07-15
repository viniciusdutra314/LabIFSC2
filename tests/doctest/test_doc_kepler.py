import matplotlib.pyplot as plt
import numpy as np

import LabIFSC2 as lab


def test_doc_kepler() -> None:
    # fmt: off
    # --8<-- [start:kepler_regressao]
    dados: list[dict[str, str | float]] = [
        {"planeta": "Mercúrio", "distancia": 36.0, "periodo": 88.0},
        {"planeta": "Vênus", "distancia": 67.2, "periodo": 224.7},
        {"planeta": "Terra", "distancia": 93.0, "periodo": 365.2},
        {"planeta": "Marte", "distancia": 141.6, "periodo": 687.0},
        {"planeta": "Júpiter", "distancia": 483.7, "periodo": 4331.0},
        {"planeta": "Saturno", "distancia": 889.8, "periodo": 10747.0},
        {"planeta": "Urano", "distancia": 1781.5, "periodo": 30589.0},
        {"planeta": "Netuno", "distancia": 2805.5, "periodo": 59800.0},
    ]
    distancias = lab.arrayM(
        [float(planeta["distancia"]) for planeta in dados], "Mmiles", 0
    )
    periodos = lab.arrayM([float(planeta["periodo"]) for planeta in dados], "days", 0)
    fitting = lab.regressao_potencia(distancias, periodos)
    assert fitting.potencia.fmt() == "(1,4979 ± 0,0008)"
    G = lab.constantes.Newtonian_constant_of_gravitation
    pi = lab.constantes.pi
    massa_sol = lab.constantes.solar_mass
    constante_teorica = np.sqrt(4 * pi**2 / (G * massa_sol))
    assert constante_teorica.fmt(unidade="si") == (
        "(5,4540 ± 0,0001) × 10⁻¹⁰ s/m¹⋅⁵"
    )
    assert fitting.amplitude.fmt(unidade="si") == "(5,8 ± 0,1) × 10⁻¹⁰ s"
    # --8<-- [end:kepler_regressao]
    # fmt: on

    # fmt: off
    # --8<-- [start:kepler_amostragem]
    unidade_x = "astronomical_unit"
    unidade_y = "years"

    x = lab.linspaceM(0, 30, 100, "astronomical_unit", 0)
    amostragem = fitting(x)
    # --8<-- [end:kepler_amostragem]
    # fmt: on
    assert np.allclose(
        lab.nominais(amostragem, unidade_y),
        [
            0.0,
            0.16720236,
            0.47222204,
            0.86677871,
            1.33367488,
            1.86297947,
            2.44799678,
            3.08382118,
            3.76665199,
            4.49338729,
            5.26151605,
            6.06894605,
            6.91380503,
            7.7943936,
            8.70950132,
            9.6576868,
            10.637894,
            11.64919283,
            12.6904141,
            13.76086203,
            14.85993445,
            15.98652,
            17.14022277,
            18.32023888,
            19.5262253,
            20.7574556,
            22.01355905,
            23.29377595,
            24.59812236,
            25.92529963,
            27.27589755,
            28.64912586,
            30.04414761,
            31.46106333,
            32.90057751,
            34.35997688,
            35.84108923,
            37.34286772,
            38.8647287,
            40.40618418,
            41.96774186,
            43.54918181,
            45.1495475,
            46.77017268,
            48.40808983,
            50.06563503,
            51.74134587,
            53.43456287,
            55.14656257,
            56.8772764,
            58.62478682,
            60.38904278,
            62.17100623,
            63.97154288,
            65.78745354,
            67.62110684,
            69.47029197,
            71.3363668,
            73.22010168,
            75.11830551,
            77.03396015,
            78.96476666,
            80.91117912,
            82.87311834,
            84.85279027,
            86.84630189,
            88.85517283,
            90.88003283,
            92.91871024,
            94.97238155,
            97.04086489,
            99.12494062,
            101.22470506,
            103.33573288,
            105.46558935,
            107.60652663,
            109.76323664,
            111.93360799,
            114.1169974,
            116.31588584,
            118.5287959,
            120.75651541,
            122.99423608,
            125.24817432,
            127.51591977,
            129.79705056,
            132.08950466,
            134.39633912,
            136.71555037,
            139.05241296,
            141.39816295,
            143.75757548,
            146.13123689,
            148.51706457,
            150.91355481,
            153.32539889,
            155.74978066,
            158.18744411,
            160.63534066,
            163.09497686,
        ],
        atol=0.5,
    )

    # fmt: off
    # --8<-- [start:kepler_grafico]
    plt.style.use("ggplot")
    plt.plot(
        lab.nominais(x, unidade_x),
        lab.nominais(amostragem, unidade_y),
        color="red",
        label="Teórica",
    )
    plt.scatter(
        lab.nominais(distancias, unidade_x),
        lab.nominais(periodos, unidade_y),
        color="blue",
        label="Dados",
    )
    plt.xlabel(f"Distâncias ({unidade_x})")
    plt.ylabel(f"Períodos ({unidade_y})")
    plt.legend()
    plt.savefig("docs/images/kepler.jpg", dpi=300)
    plt.cla()
    # --8<-- [end:kepler_grafico]
    # fmt: on

    # fmt: off
    # --8<-- [start:kepler_curvas]
    assert np.allclose(
        lab.curva_min(amostragem, "years")[0:5],
        [0.0, 0.15783305, 0.44541954, 0.81721102, 1.25700057],
        atol=1e-2,
    )
    assert np.allclose(
        lab.curva_max(amostragem, "years")[0:5],
        [0.0, 0.17670968, 0.4994268, 0.91709789, 1.41152222],
        atol=1e-2,
    )
    # --8<-- [end:kepler_curvas]
    # fmt: on
