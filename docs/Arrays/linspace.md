:::LabIFSC2.arrayM.linspace

## Exemplos
```{.py title=Exemplo com incerteza no tempo}
    import LabIFSC2 as lab
    import numpy as np
    a=1 ; b=5 ; N=1_000
    tempo=lab.linspace(a,b,N,0.1,'s')
    #print(tempo) # [(1.0±0.1)s ... (2.0±0.1)s...(5.0±0.1)s]
    print(tempo**2) #[(1.0±0.2)s... (4.0±0.4)s ... (25±1)s]
```