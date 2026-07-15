import LabIFSC2 as lab


def test_doc_sorted_list() -> None:
    # fmt: off
    # --8<-- [start:ordenacao]
    voltagens = lab.arrayM([1, 4, 3], "ampere", 0.1)
    voltagem_a = voltagens[0]
    voltagem_b = voltagens[1]

    assert max(voltagens).fmt() == "(4,0 ± 0,1) A"
    assert min(voltagens).fmt() == "(1,0 ± 0,1) A"
    assert str(sorted(voltagens)) == "[(1,0 ± 0,1) A, (3,0 ± 0,1) A, (4,0 ± 0,1) A]"
    assert voltagem_a < voltagem_b
    assert not voltagem_a > voltagem_b
    # --8<-- [end:ordenacao]
    # fmt: on
