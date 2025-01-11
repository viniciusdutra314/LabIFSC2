import sys
import os
import importlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

lab = importlib.import_module('LabIFSC2')
c=lab.constantes.speed_of_light_in_vacuum
UA=lab.constantes.astronomical_unit
tempo=UA/c
tempo.converter_para('minute')
print(tempo)
assert (8.31- tempo.nominal)<1e-2 
