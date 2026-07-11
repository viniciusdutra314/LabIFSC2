import LabIFSC2 as lab


def test_doc_lei_de_hook() -> None:
    import matplotlib.pyplot as plt

    forças = lab.linspaceM(0, 10, 10, "N", 0.1)  # variando a força
    deslocamentos = lab.arrayM(
        [0, 0.5, 1.1, 1.6, 2, 2.3, 2.8, 3.2, 3.7, 4], "cm", 0.01
    )  # medindo deslocamentos

    reta = lab.regressao_linear(deslocamentos, forças)
    a, b = reta
    assert (
        str(reta) == "AjustePolinomial(grau=1, coeficientes=[(-3 ± 2)x10⁻¹ kg·m/s², "
        "(2,51 ± 0,06)x10² kg/s²])"
    )
    assert f"Constante da mola {a:si}" == "Constante da mola (2,51 ± 0,06)x10² kg/s²"

    unidade_x = "cm"
    unidade_y = "N"

    plt.style.use("ggplot")

    plt.scatter(
        lab.nominais(deslocamentos, unidade_x),
        lab.nominais(forças, unidade_y),
        label="Dados",
        color="red",
    )

    x = lab.linspaceM(0, 4, 100, unidade_x, 0)

    plt.plot(
        lab.nominais(x, unidade_x),
        lab.nominais(reta(x), unidade_y),
        label="Regressão linear",
        color="blue",
    )

    plt.xlabel(f"Deslocamento ({unidade_x})")
    plt.ylabel(f"Força ({unidade_y})")
