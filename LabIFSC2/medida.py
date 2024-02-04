import numpy as np
from .unidades import TODAS_UNIDADES, Unidade
from .formatacoes import *

def montecarlo(func : callable, *parametros):
    '''## Propagação de erros usando Monte Carlo

  Calcula a média e desvio padrão da densidade de probabilidade de uma 
  função com variáveis gaussianas, também armazena o histograma
  inteiro dentro de uma Medida

  Globals:
    num_montecarlo : Quantidade de números aleatórios usados (Default=10.000)
    pode ser alterado globalmente usando num_montecarlo(valor)
  
  Args:
    func (callable): função para a propagação do erro
    parametros list[Medida]: parâmetros da função definida acima

  Returns:
    Resultado (Medida):  Medida com \(\mu\), \(\sigma\) e histograma
'''
    #from . import num_gaussianos

    N=int(1e4)
    if not callable(func): raise TypeError("Func precisa ser um callable")
    x_samples=np.empty((len(parametros),N))
    for index,parametro in enumerate(parametros):
        if not isinstance(parametro,Medida): 
            raise TypeError("Todos os parametros precisam ser Medidas")
        if not len(parametro.histograma):
            x_samples[index]=np.random.normal(parametro.nominal,
                                              parametro.incerteza,size=N)
        else:
            x_samples[index]=parametro.histograma
    vec_func=np.vectorize(func)
    histograma=vec_func(*x_samples)
    mean=np.mean(histograma)
    std=np.std(histograma)
    return Medida(mean,std,histograma=histograma)

class Medida:
    def __init__(self,nominal,incerteza=0,
                 unidade="",histograma=np.array([])):
        """
        Inicializa uma instância da classe Medida com um valor nominal, incerteza e unidade.
        Valor numérico se entende como qualquer objeto que possa interagir normalmente com floats,

        Parâmetros:
            - nominal: Um valor numérico que representa o valor nominal da medida.
            - incerteza: Um valor numérico que representa a incerteza associada à medida.
            - unidade: Uma string que descreve a unidade da medida.

        Raises:
            - TypeError: Se o nominal ou incerteza não puderem ser convertidos para um número.
            - TypeError: A unidade precisa ser uma string
        """
        if hasattr(nominal,'__float__'): self.nominal=nominal
        else: raise TypeError("Valor nominal inválido, é necessário um objeto que possa ser convertido para float")
        
        if hasattr(incerteza,'__float__'): self.incerteza=incerteza
        else: raise TypeError("Incerteza inválida, é necessário um objeto que possa ser convertido para float")

        if incerteza<0:
            raise ValueError("Incerteza não pode ser negativa")

        if not isinstance(histograma,np.ndarray):
            raise TypeError('Histograma deve ser um array numpy')
        else:self.histograma=histograma

        if not unidade: 
            self.unidade=TODAS_UNIDADES[""]
        elif isinstance(unidade,str):
            if unidade not in TODAS_UNIDADES:
                raise ValueError(f'Unidade {unidade} não registrada em TODAS_UNIDADES')
            self.unidade=TODAS_UNIDADES[unidade]
        else: raise TypeError('Unidade precisar uma string')
        
        if self.unidade.simbolo:
            self.si_nominal=self.nominal*self.unidade.cte_mult +self.unidade.cte_ad
            self.si_incerteza=self.incerteza*self.unidade.cte_mult
        else:
            self.si_nominal=self.nominal
            self.si_incerteza=self.incerteza
    def __str__(self):
        return self.__format__('')
    def __repr__(self):
        nominal=self.nominal
        incerteza=self.incerteza
        unidade=self.unidade.simbolo
        return f"Medida({nominal=},{incerteza=},{unidade=})"
    def __format__(self,fmt):
        import re
        padrao = re.compile(r'E(-?\d+)')
        correspondencia=re.search(padrao,fmt)
        if correspondencia:
            ordem_de_grandeza=int(correspondencia.group(1))
        else:
            ordem_de_grandeza=int(np.log10(np.abs(self.nominal)))
        nominal=self.nominal/(10**ordem_de_grandeza)
        incerteza=self.incerteza/(10**ordem_de_grandeza) 
        if 'full' not in fmt and incerteza:
            incerteza=arredondar_incerteza(incerteza)
            nominal=arredondar_nominal(nominal,float(incerteza))
        if not incerteza:
            nominal=float(nominal)
            if nominal==int(nominal): nominal=str(int(nominal))
            
        if 'latex' in fmt:
            return formatar_medida_latex(nominal,incerteza,
                                         self.unidade,ordem_de_grandeza)
        else:
            return formatar_medida_console(nominal,incerteza,
                                    self.unidade,ordem_de_grandeza)

    def __neg__(self):
        return Medida(-self.nominal,self.incerteza)
    def __eq__(self,outro):
        '''True = Equivalentes
           False = Diferentes
           None  = Inconclusivo'''
        outro=self._torna_medida(outro)
        self._checa_dimensao(outro.unidade.simbolo)
        delta_nominal=abs(self.si_nominal - outro.si_nominal)
        delta_incerteza=abs(self.si_incerteza + outro.si_incerteza)
        if delta_nominal<=2*delta_incerteza: return True
        elif delta_nominal>=3*delta_incerteza: return False
        else: return None
    def __gt__(self,outro):
        outro=self._torna_medida(outro)
        self._checa_dimensao(outro.unidade.simbolo)
        if self.__eq__(outro)==False:
            return self.si_nominal > outro.si_nominal
        else: return None
    def __ge__(self,outro):
        outro=self._torna_medida(outro)
        self._checa_dimensao(outro.unidade.simbolo)
        if self.__eq__(outro)==False:
            return self.si_nominal >= outro.si_nominal
        else: return None
    def __lt__(self,outro):
        outro=self._torna_medida(outro)
        self._checa_dimensao(outro.unidade.simbolo)
        if self.__eq__(outro)==False:
            return self.si_nominal < outro.si_nominal
        else:
            return None
    def __le__(self,outro):
        outro=self._torna_medida(outro)
        self._checa_dimensao(outro.unidade.simbolo)
        if self.__eq__(outro)==False:
            return self.si_nominal <= outro.si_nominal
        else:
            return None
    def __add__(self,outro):
        #Como existe solução analítica da soma entre duas gaussianas
        #iremos usar esse resultado para otimizar o código
        if isinstance(outro,np.ndarray):
           self_broadcast=np.repeat(self,len(outro))
           return self_broadcast + outro
        outro=self._torna_medida(outro)
        self._checa_dimensao(outro.unidade.simbolo)
        media=self.si_nominal+outro.si_nominal
        desvio_padrao=np.sqrt(self.si_incerteza**2 + outro.si_incerteza**2)
        unidade=self._unidade_mais_proxima(outro.unidade,media)
        media=media*unidade.cte_mult + unidade.cte_ad
        desvio_padrao=desvio_padrao*unidade.cte_mult
        return Medida(media,desvio_padrao,unidade)
    def __radd__(self,outro):
        return self.__add__(outro)
    def __sub__(self,outro):
        if isinstance(outro,np.ndarray):
           self_broadcast=np.repeat(self,len(outro))
           return self_broadcast - outro
        outro=self._torna_medida(outro)
        media=self.nominal-outro.nominal
        desvio_padrao=np.sqrt(self.incerteza**2 + outro.incerteza**2)
        return Medida(media,desvio_padrao)
    def __rsub__(self,outro):
        outro=self._torna_medida(outro)
        media=-self.nominal+outro.nominal
        desvio_padrao=np.sqrt(self.incerteza**2 + outro.incerteza**2)
        return Medida(media,desvio_padrao)
    def __mul__(self,outro):
        if not isinstance(outro,Medida) and not isinstance(outro,np.ndarray):
            constante=outro
            return Medida(self.nominal*constante,(self.incerteza*abs(constante)))
        elif isinstance(outro,np.ndarray):
           self_broadcast=np.repeat(self,len(outro))
           return self_broadcast * outro
        else:
            return montecarlo(lambda x,y: x*y,self,outro)
    def __rmul__(self,outro):
        return self.__mul__(outro)
    def __truediv__(self, outro):
        if not isinstance(outro,Medida) and not isinstance(outro,np.ndarray):
            constante=outro
            return Medida(self.nominal/constante,(self.incerteza/abs(constante)))
        elif isinstance(outro,np.ndarray):
           self_broadcast=np.repeat(self,len(outro))
           return self_broadcast / outro
        else:
            return montecarlo(lambda x,y: x/y,self,outro)
    def __rtruediv__(self, outro):
        outro=self._torna_medida(outro)
        return montecarlo(lambda x,y: y/x,self,outro)
    def __pow__(self,outro):
        if isinstance(outro,np.ndarray):
           self_broadcast=np.repeat(self,len(outro))
           return self_broadcast ** outro
        outro=self._torna_medida(outro)
        return montecarlo(np.power,self,outro)
    def __rpow__(self,outro):
        outro=self._torna_medida(outro)
        return montecarlo(np.power,outro,self)
    def __abs__(self):
        return Medida(abs(self.nominal),self.incerteza)
    def __int__(self):
        return int(self.nominal)
    def __float__(self):
        return float(self.nominal)
    def __complex__(self):
        return complex(self.nominal)
    def _unidade_mais_proxima(self,unidade_b,valor):
        unidade_a=self.unidade
        x=abs((unidade_a.cte_mult + unidade_a.cte_ad)-valor)
        y=abs((unidade_b.cte_mult + unidade_b.cte_ad)-valor)
        if x<y: return unidade_a
        else: return unidade_b
    def _checa_dimensao(self,outra_unidade : str):
        '''Verifica se duas Medidas possuem a mesma dimensão'''
        outra_unidade=TODAS_UNIDADES[outra_unidade]
        if not np.array_equal(self.unidade.dimensao,outra_unidade.dimensao):
            raise ValueError("Medidas com dimensões diferentes")
    def converte(self,nova_unidade):
        self._checa_dimensao(nova_unidade)
        nova_unidade=TODAS_UNIDADES[nova_unidade]
        cte_mul=self.unidade.cte_mult/nova_unidade.cte_mult
        return Medida(self.nominal*cte_mul,self.incerteza*cte_mul,unidade=nova_unidade.simbolo)
    def _torna_medida(self,objeto):
        if isinstance(objeto,Medida): return objeto
        else: return Medida(objeto)
    def _checa_dimensao(self,outra_unidade : str):
        outra_unidade=TODAS_UNIDADES[outra_unidade]
        if not np.array_equal(self.unidade.dimensao,outra_unidade.dimensao):
            raise ValueError("Unidades com dimensões diferentes")
    def converte(self,outra_unidade):
        self._checa_dimensao(outra_unidade)
        outra_unidade=TODAS_UNIDADES[outra_unidade]
        cte_mul=self.unidade.cte_mult/outra_unidade.cte_mult
        return Medida(self.nominal*cte_mul,self.incerteza*cte_mul,unidade=outra_unidade.simbolo)
    def _torna_medida(self,objeto):
        if isinstance(objeto,Medida): return objeto
        else: return Medida(objeto)
    def probabilidade(m,a,b) -> float:
        ''' Retorna a probabilidade que a Medida
        esteja entre [a,b] usando o histograma como
        referencia

        Args:
            a (float): Extremo inferior
            b (float): Extremo superior

        Returns:
            probabilidade: (float) probabilidade de estar entre [a,b]
        
        '''

        if not len(m.histograma):
            m.histograma=np.random.normal(m.nominal,
                        m.incerteza,10_000)
        condition=np.logical_and(m.histograma>=a,m.histograma<=b)
        chance=np.count_nonzero(condition)/len(m.histograma)
        return chance


def equivalente(medida1 : Medida, medida2 : Medida, sigmas : float ):
    '''Critério de equivalência customizável, escolha
    até quantos sigmas duas Medidas são consideradas iguais
    (Na classe Medida, por padrão são 2 sigmas)

    Exemplo:
        x=Medida(1.0 , 0.05)
        y=Medida(0.7, 0.05)
        
        x.equivalente(y,3) # True

        x - y = 0.3 +- 0.1
        Com dois sigmas elas são consideradas diferentes,
        porém com 3 sigmas elas são equivalentes
    '''
    if not isinstance(medida1,Medida) or not isinstance(medida2,Medida):
        raise TypeError("Ambos valores precisam ser Medidas")
    
    try: sigmas=float(sigmas)
    except: raise TypeError("É necessário especificar uma quantidade de sigmas")
    delta_nominal=abs(medida1.nominal - medida2.nominal)
    delta_incerteza=abs(medida1.incerteza + medida2.incerteza)
    return delta_nominal<=sigmas*delta_incerteza

