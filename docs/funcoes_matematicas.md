## Operações Elementares

A classe `Medida` implementa todas as operações matemáticas elementares. Portanto, operações entre instâncias de `Medida` são idênticas a operações entre números.

```py
--8<-- "tests/doctest/test_doc_operacoes_basicas.py:operacoes_basicas"
```

## Funções Numpy

O LabIFSC2 implementa uma compatibilidade direta com as funções do Numpy (tecnicamente chamadas de [ufunc](https://numpy.org/doc/stable/reference/ufuncs.html)), permitindo que você aplique funções como `np.sin`, `np.sqrt`, `np.arctanh` de forma natural[^1].

```py
--8<-- "tests/doctest/test_doc_sqrt_vetorizado.py:code"

```

Veja que as unidades se comportam como o esperado. Outro exemplo interessante é a função seno, em que podemos usar diretamente o resultado em graus, sem precisar converter para radianos.

```py
--8<-- "tests/doctest/test_doc_seno.py:seno"
```

[^1]:
    Para os curiosos, o numpy tem uma seção inteira na sua [documentação](https://numpy.org/doc/stable/user/basics.interoperability.html#) sobre como usar funções numpy em objetos
    arbitrários e até como implementar o seu próprio tipo array
