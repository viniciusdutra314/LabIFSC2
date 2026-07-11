import LabIFSC2 as lab


def test_doc_histograma() -> None:
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.axes import Axes
    from matplotlib.gridspec import GridSpec
    from numpy.typing import ArrayLike
    from pint import Quantity
    from scipy.stats import norm  # type: ignore[import-untyped]

    # Definindo as lab.constantes e medidas
    pi = lab.constantes.pi
    L = lab.Medida(15, "cm", 1)
    T = lab.Medida(780, "ms", 80)
    gravidade = (4 * pi**2) * L / T**2
    histograma_g = gravidade.histograma
    histograma_L = L.histograma
    histograma_T = T.histograma
    assert isinstance(histograma_g, Quantity)
    assert isinstance(histograma_L, Quantity)
    assert isinstance(histograma_T, Quantity)

    # Configurando o estilo do plot
    plt.style.use("ggplot")

    # Criando a grade personalizada
    fig = plt.figure(figsize=(10, 8))
    gs = GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1])

    # Adicionando os subplots à grade
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])

    # Função para ajustar e plotar uma gaussiana
    def plot_gaussian(ax: Axes, data: ArrayLike, color: str) -> None:
        mu, std = norm.fit(data)
        xmin, xmax = ax.get_xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        ax.plot(x, p, color=color, linestyle="--", linewidth=2)

    # Histograma de L
    ax1.hist(histograma_L, bins=100, color="green", alpha=0.7, density=True)
    ax1.set_title("PDF (L)")
    ax1.set_xlabel("L (cm)")
    ax1.set_ylabel("Frequência")
    plot_gaussian(ax1, histograma_L, "green")

    # Histograma de T
    ax2.hist(histograma_T, bins=100, color="red", alpha=0.7, density=True)
    ax2.set_title("PDF (T)")
    ax2.set_xlabel("T (ms)")
    ax2.set_ylabel("Frequência")
    plot_gaussian(ax2, histograma_T, "red")

    # Histograma da gravidade
    ax3.hist(histograma_g.to("m/s²"), bins=100, color="blue", alpha=0.7, density=True)
    ax3.set_title(r"PDF ($g=\frac{4\pi^2L}{T^2}$)")
    ax3.set_xlabel("g (m/s²)")
    ax3.set_ylabel("Frequência")
    plot_gaussian(ax3, histograma_g.to("m/s²"), "blue")

    # Ajustando o layout
    plt.tight_layout()
    plt.savefig("docs/images/gravidade_histograma.jpg", dpi=300)
    plt.close(fig)
