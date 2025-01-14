from LabIFSC2._tipagem_forte import obrigar_tipos
import LabIFSC2 as lab
import numpy as np
from collections.abc import Sequence
from numbers import Number
from fractions import Fraction
from decimal import Decimal
import pytest

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

def test_sequence_array_com_subtipos():
    @obrigar_tipos
    def recebe_sequence(x:Sequence[Number],y:Sequence[Number]) -> Sequence[Number]: return [1,2,3,4]

    x=[1,2,3]
    y=[4,5,6]
    recebe_sequence(x,y)
    recebe_sequence((1,2,3),(4,5,6))
    with pytest.raises(TypeError): recebe_sequence(1,2)
    with pytest.raises(TypeError): recebe_sequence(['1'],['2'])

    @obrigar_tipos
    def recebe_array_numpy(x:np.ndarray[Number],y:np.ndarray[Number]) -> np.ndarray[Number]: return np.array([1,2,3,4])
    x=np.array([1,2,3])
    y=np.array([4,5,6])
    recebe_array_numpy(x,y)
    with pytest.raises(TypeError): recebe_array_numpy(1,2)
    with pytest.raises(TypeError):recebe_array_numpy([1,2,3],[2])
    with pytest.raises(TypeError):recebe_array_numpy(np.array(['hey','a']),np.array(['hey','a']))
    
    @obrigar_tipos
    def recebe_array_de_medidas(x:np.ndarray[lab.Medida])-> np.ndarray[Number]:
        return np.array([1,2,3,4,5])
    medidas=lab.linspace(1,10,10,3,'m')
    recebe_array_de_medidas(medidas)
    with pytest.raises(TypeError):recebe_array_de_medidas(np.array([1,2,3,4,5]))
    with pytest.raises(TypeError):recebe_array_de_medidas(medidas.tolist())
