import LabIFSC2 as lab

c=lab.constantes.speed_of_light_in_vacuum
UA=lab.constantes.astronomical_unit

tempo=UA/c

print(f"{tempo:minute}") #8,316746397269273671781775192 min
assert (8.31- tempo.nominal('minute'))<1e-2 