from collections.abc import Sequence
from decimal import Decimal
from fractions import Fraction
from numbers import Number
from typing import Any

import numpy as np
import pytest

import LabIFSC2 as lab
from LabIFSC2._tipagem_forte import obrigar_tipos


def test_obrigar_tipos():
    @obrigar_tipos
    def soma_simples(x:Number,y:Number) -> Number: return x + y 
    with pytest.raises(TypeError): soma_simples(1,'2')
    with pytest.raises(TypeError): soma_simples('1',2)
    soma_simples(0.3,1)
    soma_simples(Fraction(5,2),3)
    soma_simples(Decimal('0.431'),3)
    soma_simples(np.float64(0.3),np.int32(3))
    @obrigar_tipos
    def soma_simples_retorno_errado(x:Number,y:Number) -> Number: return '3'
    with pytest.raises(TypeError):
        soma_simples_retorno_errado(1,2)

def test_sequence_arrays():
    @obrigar_tipos
    def recebe_sequence(x:Sequence,y:Sequence) -> Sequence: return [1,2,3,4]

    x=[1,2,3]
    y=[4,5,6]
    recebe_sequence(x,y)
    recebe_sequence((1,2,3),(4,5,6))
    with pytest.raises(TypeError): recebe_sequence(1,2)
    with pytest.raises(TypeError): recebe_sequence(np.array([1,2,3]),np.array([2]))

    @obrigar_tipos
    def recebe_array_numpy(x:np.ndarray,y:np.ndarray) -> np.ndarray: return np.array([1,2,3,4])
    x=np.array([1,2,3])
    y=np.array([4,5,6])
    recebe_array_numpy(x,y)
    with pytest.raises(TypeError): recebe_array_numpy(1,2)
    with pytest.raises(TypeError): recebe_array_numpy([1,2,3],[2])


def test_union_types():

    @obrigar_tipos
    def multiplicacao_union(x: Number | lab.Medida, y: Number | lab.Medida) -> Number | lab.Medida:
        return x * y

    # Valid cases
    multiplicacao_union(1, 2)
    multiplicacao_union(Fraction(1, 2), 2)
    multiplicacao_union(Decimal('0.5'), 1)
    medidas = lab.linspaceM(1, 10, 10, 'm', 3)
    multiplicacao_union(medidas[0], medidas[1])
    multiplicacao_union(1, medidas[0])

    # Invalid cases
    with pytest.raises(TypeError): multiplicacao_union(1, '2')
    with pytest.raises(TypeError): multiplicacao_union('1', 2)
    with pytest.raises(TypeError): multiplicacao_union(medidas[0], '2')
    with pytest.raises(TypeError): multiplicacao_union('1', medidas[0])



def test_classe():

    class Exemplo:
        @obrigar_tipos
        def __init__(self, x: Number, y: Number):
            self.x = x
            self.y = y
        @obrigar_tipos
        def multiplica(self:'Exemplo',x:Number,y:Number) -> Number:
            return x*y
    x=Exemplo(1,2)
    with pytest.raises(TypeError): Exemplo('1', 2)
    x.multiplica(4,3)
    with pytest.raises(TypeError): x.multiplica([2],3)