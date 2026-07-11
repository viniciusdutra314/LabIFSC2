import LabIFSC2 as lab


def test_doc_grafico_fitting() -> None:
    import matplotlib.pyplot as plt

    campo_magnético = lab.arrayM([210, 90, 70, 54, 39, 32, 33, 27, 22, 20], "muT", 1)
    distancias = lab.linspaceM(1, 10, 10, "cm", 0.01)

    unidade_x = "cm"
    unidade_y = "muT"

    fitting = lab.regressao_potencia(distancias, campo_magnético)
    plt.style.use("ggplot")
    plt.errorbar(
        x=lab.nominais(distancias, unidade_x),
        y=lab.nominais(campo_magnético, unidade_y),
        xerr=lab.incertezas(distancias, unidade_x),
        yerr=lab.incertezas(campo_magnético, unidade_y),
        fmt="o",
        label="Dados experimentais",
        color="red",
    )

    # fmt: off
    # --8<-- [start:grafico_fitting]
    x = lab.linspaceM(1, 10, 100, unidade_x, 0)
    amostragem = fitting(x)
    plt.plot(
        lab.nominais(x, unidade_x),
        lab.nominais(amostragem, unidade_y),
        color="blue",
        label="Curva teórica",
    )
    plt.fill_between(
        x=lab.nominais(x, unidade_x),
        y1=lab.curva_min(amostragem, unidade_y),
        y2=lab.curva_max(amostragem, unidade_y),
        color="blue",
        alpha=0.3,
    )
    # --8<-- [end:grafico_fitting]
    # fmt: on
    plt.legend()
    plt.savefig("docs/images/graficos_fitting.jpg", dpi=300)
    plt.cla()
