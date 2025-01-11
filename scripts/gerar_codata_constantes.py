'''Script usado na criação do arquivo constantes/constantes.py
Ele essencialmente baixa as constantes definidas pela CODATA
e transforma o arquivo .txt em variáveis python acessíveis
pelo submódulo
'''

import os
import urllib.request
import io

file_name='codata_constantes.txt'
abs_path=os.path.dirname(__file__)
file_dir=os.path.join(abs_path,file_name)

url = "https://physics.nist.gov/cuu/Constants/Table/allascii.txt"
response = urllib.request.urlopen(url)
content = response.read()

file_like_object = io.BytesIO(content)

with file_like_object as txt:
    #esses números mágicos fazem muito sentido se
    #você abrir o arquivo de texto
    lines = txt.read().decode('utf-8').splitlines()[11:]
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

with open('../LabIFSC2/constantes/constantes.py','w') as python_arquivo:
    python_arquivo.write("'''Aqui são guardadas as constantes da natureza usadas no LabIFSC2 ,\n \
    caso queira adicionar uma nova constante, é  interessante que \n \
    o nome esteja em inglês,siga a ordem alfabética para a tabela \n \
    permanecer organizada e preencha corretamente os campos de \n \
    valor nominal,incerteza e unidade.  \n \
\n \
    Sinta-se livre para realizer um pull-request no repositório, só não \n \
    se esqueça de por favor referenciar a fonte que você usou para \n \
    encontrar a constante (toda essa tabela é baseada na CODATA2022)'''\n"
    )

    python_arquivo.write('from LabIFSC2 import Medida\n')
    for name, values in constantes_dict.items():
        python_arquivo.write(f'{name}=Medida{values[0],values[1],values[2]}\n')
    python_arquivo.write('pi=3.14159265358979323846\n')
    python_arquivo.write('euler=2.7182818284590452353602874713527\n')
    python_arquivo.write('golden_ratio=1.61803398874989484820458\n')
    python_arquivo.write('astronomical_unit=Medida(149_597_870_700,0,"m")\n')