A função `Incertezas` recebe um objeto iterável, como um ndarray, lista, tupla, etc., contendo objetos do tipo `Medida`. Ela retorna um numpy array com todas as incertezas das medidas contidas no iterável.
```python3
    from LabIFSC2 import *
    import numpy as np
    #Crie um array numpy com Medidas
    array = np.array([Medida(4, 0.2), Medida(35, 3), Medida(-97, 1)])
    incertezas_array = Incertezas(array)  # ndarray([0.2, 3.0, 1.0])
```
 