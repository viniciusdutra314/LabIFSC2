from LabIFSC2 import *


def test_doc_grafico_fitting() -> None:
    import matplotlib.pyplot as plt

    campo_magnético = arrayM([210, 90, 70, 54, 39, 32, 33, 27, 22, 20], "muT", 1)
    distancias = linspaceM(1, 10, 10, "cm", 0.01)

    unidade_x = "cm"
    unidade_y = "muT"

    fitting = regressao_potencia(distancias, campo_magnético)
    plt.style.use("ggplot")
    plt.errorbar(
        x=nominais(distancias, unidade_x),
        y=nominais(campo_magnético, unidade_y),
        xerr=incertezas(distancias, unidade_x),
        yerr=incertezas(campo_magnético, unidade_y),
        fmt="o",
        label="Dados experimentais",
        color="red",
    )

    x = linspaceM(1, 10, 100, unidade_x, 0)
    amostragem = fitting(x)
    plt.plot(
        nominais(x, unidade_x),
        nominais(amostragem, unidade_y),
        color="blue",
        label="Curva teórica",
    )
    plt.fill_between(
        x=nominais(x, unidade_x),
        y1=curva_min(amostragem, unidade_y),
        y2=curva_max(amostragem, unidade_y),
        color="blue",
        alpha=0.3,
    )
    plt.legend()
    plt.savefig("docs/images/graficos_fitting.jpg", dpi=300)
    plt.cla()
