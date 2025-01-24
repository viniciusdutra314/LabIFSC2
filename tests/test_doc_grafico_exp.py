import matplotlib.pyplot as plt
import numpy as np

x=np.linspace(0,2,1000)
y=np.exp(x)
plt.plot(x,y)

plt.savefig('docs/images/exponencial.jpg',dpi=200)
plt.cla()