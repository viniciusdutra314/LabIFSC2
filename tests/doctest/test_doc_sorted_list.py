from LabIFSC2 import *


def test_doc_sorted_list():
    voltagens = arrayM([1, 4, 3], "ampere", 0.1)
    voltagem_a = voltagens[0]
    voltagem_b = voltagens[1]

    assert str(max(voltagens)) == "(4,0 ± 0,1) A"
    assert str(min(voltagens)) == "(1,0 ± 0,1) A"
    assert str(sorted(voltagens)) == "[(1,0 ± 0,1) A, (3,0 ± 0,1) A, (4,0 ± 0,1) A]"
    assert voltagem_a < voltagem_b
    assert not voltagem_a > voltagem_b
