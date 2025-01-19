## Operações elementares
A classe Medida implementa todas as operações matemáticas elementares,
portanto, operações entre Medidas são idênticas a operações entre números 

```py
--8<-- "tests/test_doc_operacoes_basicas.py:1:10"
```

## Decorador Aceita Medida
Pela generalidade do método de propagação de erros usando monte carlo, o LabIFSC2 possui uma decorador 
que consegue fazer com que uma função matemática **qualquer do numpy** aceite uma `Medida` e faça propagação de erros, 
essa é a magia do `aceitamedida`


```py 
--8<-- "tests/test_doc_aceitamedida.py:1:11"
```

Perceba que pegamos a função do numpy (np.sin) e transformamos ela em uma função que aceita medidas, 
temos ainda integrações bonitas com o sistema de unidades, conseguimos usar um ângulo diretamente em **graus** 
sem converter para radianos.

## Operando em arrays

As funções além de aceitarem medidas também aceitam arrays numpy, podemos fazer então operações
vetorizadas

```py 
--8<-- "tests/test_doc_sqrt_vetorizado.py:1:8"
```

## Todas funções suportadas
Caso queira uma lista de todas as funções matemáticas que estão no LabIFSC2, eis o código fonte com todas elas e seus apelidos (sin=seno, tan=tg)
```py {title=_matematica.py}
--8<-- "LabIFSC2/_matematica.py:39"
```
