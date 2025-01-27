from LabIFSC2 import *


def test_doc_sorted_list():
    voltagens=arrayM([1,4,3],'ampere',0.1)
    print(max(voltagens)) #(4,0 ± 0,1) A
    print(min(voltagens)) #(1,0 ± 0,1) A
    print(sorted(voltagens)) #[(1,0 ± 0,1) A, (3,0 ± 0,1) A, (4,0 ± 0,1) A]``

    voltagem_a=voltagens[0]
    voltagem_b=voltagens[1]
    print(voltagem_a<voltagem_b) #True
    print(voltagem_a>voltagem_b) #False

    assert str(max(voltagens))=='(4,0 ± 0,1) A'
    assert str(min(voltagens))=='(1,0 ± 0,1) A'
    assert str(sorted(voltagens))=='[(1,0 ± 0,1) A, (3,0 ± 0,1) A, (4,0 ± 0,1) A]'
    assert voltagem_a<voltagem_b
    assert not voltagem_a>voltagem_b