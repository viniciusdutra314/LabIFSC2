:::LabIFSC2.arrayM.get_nominais
## Exemplos
```python3
    import LabIFSC2 as lab
    import numpy as np
    #Crie um array numpy com Medidas
    array = np.array([Medida(4, 0.2), Medida(35, 3), Medida(-97, 1)])
    nominais_array = lab.get_nominais(array)  # ndarray([4,35,-97])
```
