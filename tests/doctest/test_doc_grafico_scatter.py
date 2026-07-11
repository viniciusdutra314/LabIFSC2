import LabIFSC2 as lab


def test_doc_grafico_scatter() -> None:
    import matplotlib.pyplot as plt

    # fmt: off
    # --8<-- [start:grafico_scatter]
    campo_magnético = lab.arrayM([250, 150, 110, 90, 70, 60, 55, 40, 25, 20], "muT", 10)
    distancias = lab.linspaceM(1, 10, 10, "cm", 0.5)

    unidade_x = "cm"
    unidade_y = "muT"

    plt.style.use("ggplot")
    plt.errorbar(
        x=lab.nominais(distancias, unidade_x),
        y=lab.nominais(campo_magnético, unidade_y),
        xerr=lab.incertezas(distancias, unidade_x),
        yerr=lab.incertezas(campo_magnético, unidade_y),
        fmt="o",
    )

    plt.xlabel(f"Distancia ({unidade_x})")
    plt.ylabel(f"Campo magnético ({unidade_y})")
    plt.savefig("docs/images/graficos_scatter.jpg", dpi=300)
    plt.cla()
    # --8<-- [end:grafico_scatter]
    # fmt: on
