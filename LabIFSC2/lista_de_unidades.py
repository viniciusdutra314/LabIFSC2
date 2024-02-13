import numpy as np

from .sistema_de_unidades import Unidade

Unidade("adimensional","","",[0,0,0,0,0,0,0])
#Adicione sua unidade nova aqui:
Unidade('kilograma','kg','kg',[0,0,1,0,0,0,0])
##carga
Unidade("Coulomb","C","C",[1,0,0,1,0,0,0])
Unidade("Carga elementar","e","e",[1,0,0,1,0,0,0],1.602176634e-19)
Unidade("miliampere-hora","mAh","mAh",[1,0,0,1,0,0,0],3.6)
Unidade("ampere-hora","Ah","Ah",[1,0,0,1,0,0,0],3_600)
##corrente
Unidade("Ampere", "A", "A", [0,0,0,1,0,0,0])
#distâncias 
Unidade("kilometro","km","km",[0,1,0,0,0,0,0],1e3)
Unidade("metro","m","m",[0,1,0,0,0,0,0])
Unidade("centimetro","cm","cm",[0,1,0,0,0,0,0],1e-2)
Unidade("milimetro","mm","mm",[0,1,0,0,0,0,0],1e-3)
Unidade("micrometro","um","μm",[0,1,0,0,0,0,0],1e-6)
Unidade("micrometro","μm","μm",[0,1,0,0,0,0,0],1e-6)
Unidade("nanometro","nm","nm",[0,1,0,0,0,0,0],1e-9)
#distâncias-imperial
Unidade("polegada","in","in",[0,1,0,0,0,0,0],0.0254)
Unidade("pé","ft","ft",[0,1,0,0,0,0,0],0.3048)
Unidade("jarda","yd","yd",[0,1,0,0,0,0,0],0.9144)
Unidade("milhas","mi","mi",[0,1,0,0,0,0,0],1.609344)
#distâncias-astronomia
Unidade("ano luz","ly","ly",[0,1,0,0,0,0,0], 9460730472580800)
Unidade("parsec","pc","pc",[0,1,0,0,0,0,0],3.085677581e16)
Unidade("unidade astronomica","au","au",[0,1,0,0,0,0,0],149597870700)
##Energia
Unidade("Joule","J","J",[-2,2,1,0,0,0,0])
Unidade("Caloria","cal","cal",[-2,2,1,0,0,0,0],4184)
Unidade("Quilowatt-hora","kWh","kWh",[-2,2,1,0,0,0,0],3.6e6)
Unidade("ElectronVolt","eV","eV",[-2,2,1,0,0,0,0], 1.602176634e-19)
Unidade("Erg","erg","erg",[-2,2,1,0,0,0,0], 1e-7)
Unidade("kiloton","kt","kt",[-2,2,1,0,0,0,0], 4.184e12)
Unidade("megaton","Mt","Mt",[-2,2,1,0,0,0,0], 4.184e15)
Unidade("gigaton","Gt","Gt",[-2,2,1,0,0,0,0], 4.184e18)
#Força
Unidade("Newton","N","N",[-2,1,1,0,0,0,0])
Unidade("Dina","Dyn","Dyn",[-2,1,1,0,0,0,0],1e-5)

#Pressão
Unidade("Pascal","Pa","Pa",[-2,-1,1,0,0,0,0])
Unidade("Torr", "Torr", "Torr",[-2,-1,1,0,0,0,0],101325/760)
Unidade("milímetros de mercúrio", "mmHg", "mmHg",[-2,-1,1,0,0,0,0],133.322387415)
Unidade("centímetros de mercúrio", "cmHg", "cmHg", [-2,-1,1,0,0,0,0], 1333.22387415)
Unidade("polegadas de mercúrio", "inHg", "inHg", [-2,-1,1,0,0,0,0], 3386.39)
Unidade("Atmosfera","atm","atm",[-2,-1,1,0,0,0,0],101325)
Unidade("Pounds per Square","psi","psi",[-2,-1,1,0,0,0,0],6894.76)
Unidade("Bar","Ba","Ba",[-2,-1,1,0,0,0,0],100000)
#Potência
Unidade("Watt","W","W",[-3,-2,1,0,0,0,0])
Unidade("horse-power","hp","hp",[-3,-2,1,0,0,0,0],745.7)
Unidade("cavalo-vapor","cv","cv",[-3,-2,1,0,0,0,0],735.4987)
##Resistência elétrica
Unidade("Ohm", "Ohm", r"\Omega", [-3,3,1,-2,0,0,0])
##Temperatura
Unidade("Kelvin", "K", "K",[0,0,0,0,1,0,0])
Unidade("Celsius", "ºC", r"^\circ C",[0,0,0,0,1,0,0],0,273.15)
Unidade("Fahrenheit", "ºF", r"^\circ F",[0,0,0,0,1,0,0],5/9,255.372)
#Tempo
Unidade("segundo", "s", "s", [1,0,0,0,0,0,0]),
Unidade("minuto", "min", "min",[1,0,0,0,0,0,0] ,60)
Unidade("hora", "h", "h", [1,0,0,0,0,0,0], 3_600)
Unidade("dia", "dia", "dia", [1,0,0,0,0,0,0],86_400)
Unidade("ano comum", "ano", "ano", [1,0,0,0,0,0,0],31.536e6)
#Voltagem
Unidade("Voltagem", "V", "V", [-3,2,1,-1,0,0,0])