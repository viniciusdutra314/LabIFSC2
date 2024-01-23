:::LabIFSC2.arrayM.get_incertezas
```python3
    import LabIFSC2 as lab
    import numpy as np
    #Crie um array numpy com Medidas
    array = np.array([lab.Medida(4, 0.2),lab.Medida(35, 3), lab.Medida(-97, 1)])
    incertezas_array = lab.get_incertezas(array)  # ndarray([0.2, 3.0, 1.0])
```
 