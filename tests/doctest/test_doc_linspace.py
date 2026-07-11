from LabIFSC2 import *


def test_doc_linspace():
    distancias = linspaceM(1, 10, 10, "cm", 0.05)
    assert str(distancias) == (
        "[(1,00 ± 0,05) cm (2,00 ± 0,05) cm (3,00 ± 0,05) cm (4,00 ± 0,05) cm\n"
        " (5,00 ± 0,05) cm (6,00 ± 0,05) cm (7,00 ± 0,05) cm (8,00 ± 0,05) cm\n"
        " (9,00 ± 0,05) cm (1,000 ± 0,005)x10¹ cm]"
    )
    campo_magnético = arrayM([250, 150, 110, 90, 70, 60, 55, 40, 25, 20], "muT", 1)
    assert str(campo_magnético) == (
        "[(2,50 ± 0,01)x10² µT (1,50 ± 0,01)x10² µT (1,10 ± 0,01)x10² µT\n"
        " (9,0 ± 0,1)x10¹ µT (7,0 ± 0,1)x10¹ µT (6,0 ± 0,1)x10¹ µT\n"
        " (5,5 ± 0,1)x10¹ µT (4,0 ± 0,1)x10¹ µT (2,5 ± 0,1)x10¹ µT\n"
        " (2,0 ± 0,1)x10¹ µT]"
    )
