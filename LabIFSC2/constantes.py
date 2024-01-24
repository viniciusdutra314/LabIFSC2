import os
from subprocess import run
from .medida import Medida

abs_path=os.path.dirname(__file__)
file_name='codata2018_constantes.txt'
file_dir=os.path.join(abs_path,file_name)
if file_name not in os.listdir(abs_path):
    run(["curl","https://physics.nist.gov/cuu/Constants/Table/allascii.txt",
          "-o" ,file_dir])
with open(file_dir,'r') as txt:
    #esses números mágicos fazem muito sentido se
    #você abrir o arquivo de texto
    lines=txt.readlines()[11:]
    constantes_dict={}
    for line in lines:
        name=line[:60].rstrip().replace(" ","_")
        nominal=float(line[60:85].rstrip().replace(" ","").replace(".",""))
        incerteza=line[85:110].rstrip().replace(" ","")
        if incerteza=="(exact)": incerteza=0
        else: incerteza=float(incerteza)
        unidade=line[110:].strip()
        constantes_dict[name]=[nominal,incerteza,unidade]
