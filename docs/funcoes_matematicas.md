## Operações elementares
A classe Medida implementa todas as operações matemáticas elementares,
portanto, operações entre Medidas são idênticas a operações entre números 

```py
--8<-- "tests/test_doc_operacoes_basicas.py:1:10"
```

## Funções Numpy

O LabIFSC2 implementa uma compatibilidade direta com as funções do Numpy (tecnicamente chamadas de [ufunc](https://numpy.org/doc/stable/reference/ufuncs.html)), então você aplicar funções como np.sin, np.sqrt, np.arctanh naturalmente[^1]



```py
--8<-- "tests/test_doc_sqrt_vetorizado.py:1:8"
```

[^1]:
    Para os curiosos, isso é feito implementado métodos específicos na classe Medida, por exemplo, a função np.sqrt(x) verifica se o tipo de x tem o método x.sqrt,se tiver, ele chama x.sqrt, a classe `Medida` possui uma simulação monte carlo de sqrt e todas as funções matemáticas (isso é feito criando-se dinamicamente os métodos com [__getattr__](https://docs.python.org/3/reference/datamodel.html#object.__getattr__))