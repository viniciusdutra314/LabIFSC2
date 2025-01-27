import numpy as np

from LabIFSC2 import *


def test_min_max_python():
    tempos=linspaceM(0,10,11,'s',5813256813)
    assert max(tempos) is tempos[-1]
    assert min(tempos) is tempos[0]

    tempos=linspaceM(0,10,11,'s',0)
    assert max(tempos) is tempos[-1]
    assert min(tempos) is tempos[0]

def test_min_max_numpy():
    tempos=linspaceM(0,10,11,'s',5813256813)
    assert np.max(tempos) is tempos[-1]
    assert np.min(tempos) is tempos[0]

    tempos=linspaceM(0,10,11,'s',0)
    assert np.max(tempos) is tempos[-1]
    assert np.min(tempos) is tempos[0]

def test_sorted_numpy():
    tempos=arrayM([4,1,3,2,7,5,9,6,8,10],'s',0)
    
    assert str(np.sort(tempos)) == "[1 s 2 s 3 s 4 s 5 s 6 s 7 s 8 s 9 s 1,0x10¹ s]"
    tempos=arrayM([4,1,3,2,7,5,9,6,8,10],'s',0)
    tempos.sort()
    assert str(np.sort(tempos)) == "[1 s 2 s 3 s 4 s 5 s 6 s 7 s 8 s 9 s 1,0x10¹ s]"

def test_sorted_python():
    tempos=arrayM([4,1,3,2,7,5,9,6,8,10],'s',0)
    assert str(sorted(tempos)) == "[1 s, 2 s, 3 s, 4 s, 5 s, 6 s, 7 s, 8 s, 9 s, 1,0x10¹ s]"

