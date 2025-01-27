## Operações Elementares

A classe `Medida` implementa todas as operações matemáticas elementares. Portanto, operações entre instâncias de `Medida` são idênticas a operações entre números.

```py
--8<-- "tests/test_doc_operacoes_basicas.py:7:14"
```

## Funções Numpy

O LabIFSC2 implementa uma compatibilidade direta com as funções do Numpy (tecnicamente chamadas de [ufunc](https://numpy.org/doc/stable/reference/ufuncs.html)), permitindo que você aplique funções como `np.sin`, `np.sqrt`, `np.arctanh` de forma natural[^1].

```py
--8<-- "tests/test_doc_sqrt_vetorizado.py:5:9"
```

Veja que as unidades se comportam como o esperado. Outro exemplo interessante é a função seno, em que podemos usar diretamente o resultado em graus, sem precisar converter para radianos.



```py
--8<-- "tests/test_doc_seno.py:5:7"
```

[^1]:
    Para os curiosos, isso é feito implementando métodos específicos na classe `Medida`. Por exemplo, a função `np.sqrt(x)` verifica se o tipo de `x` tem o método `x.sqrt`. Se tiver, ele chama `x.sqrt`. A classe `Medida` possui uma simulação Monte Carlo de `sqrt` e todas as funções matemáticas. Isso é feito criando-se dinamicamente os métodos com [__getattr__](https://docs.python.org/3/reference/datamodel.html#object.__getattr__).