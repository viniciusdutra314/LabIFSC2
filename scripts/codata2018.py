'''Script usado na criação do arquivo constantes/constantes.py
Ele essencialmente baixa as constantes definidas pela CODATA2018
e transforma o arquivo .txt em variáveis python acessíveis
pelo submódulo
'''

import os
from subprocess import run

file_name='codata2018_constantes.txt'
abs_path=os.path.dirname(__file__)
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
        name=name.replace('-','_').replace('.','').replace("/","_over_")
        name=name.replace('(','').replace(')','').replace(',','')
        nominal=float(line[60:85].rstrip().replace(" ","").replace("...",""))
        incerteza=line[85:110].rstrip().replace(" ","")
        if incerteza=="(exact)": incerteza=0
        else: incerteza=float(incerteza)
        unidade=line[110:].strip()
        constantes_dict[name]=[nominal,incerteza,unidade]
with open(os.path.join(abs_path,'constantes.py'),'w') as python_arquivo:
    python_arquivo.write('from LabIFSC2 import Medida\n')
    for name, values in constantes_dict.items():
        python_arquivo.write(f'{name}=Medida{values[0],values[1],values[2]}\n')