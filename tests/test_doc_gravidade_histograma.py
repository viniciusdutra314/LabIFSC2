import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from LabIFSC2 import *

# Definindo as constantes e medidas
pi = constantes.pi
L = Medida(15, 1, 'cm')
T = Medida(780, 80, 'ms')
gravidade = (4 * pi**2) * L / T**2
histograma_g = gravidade.histograma
histograma_L = L.histograma
histograma_T = T.histograma

#(...) bastante matplotlib para ficar bonito 
plt.style.use('ggplot')

# Obtendo os histogramas


# Criando a grade personalizada
fig = plt.figure()
gs = GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1])

# Adicionando os subplots à grade
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])



# Histograma de L
ax1.hist(histograma_L, bins=1000, color='green', alpha=0.7)
ax1.set_title('PDF (L)')
ax1.set_xlabel('L (cm)')
ax1.set_ylabel('Frequência')

# Histograma de T
ax2.hist(histograma_T, bins=100, color='red', alpha=0.7)
ax2.set_title('PDF (T)')
ax2.set_xlabel('T (ms)')
ax2.set_ylabel('Frequência')

# Histograma da gravidade
ax3.hist(histograma_g.to('m/s²'), bins=1000, color='blue', alpha=0.7)
ax3.set_title(r'PDF ($g=\frac{4\pi^2L}{T^2}$)')
ax3.set_xlabel('g (m/s²)')
ax3.set_ylabel('Frequência')

# Ajustando o layout
plt.tight_layout()
plt.savefig("docs/images/gravidade_histograma.jpg",dpi=300)