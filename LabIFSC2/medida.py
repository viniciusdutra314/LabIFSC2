import numpy as np
from .unidades import TODAS_UNIDADES, Unidade

def montecarlo(func : callable, *parametros  , 
               hist : bool=False,probabilidade : list[float] =[0,0]):
    '''Propagação de erros usando Monte Carlo

  Calcula a média e desvio padrão da densidade de probabilidade de uma 
  função com variaveis gaussianas, é possível calcular a probabilidade de o 
  resultado estar entre [a,b], como também,  receber os valores calculados 
  para que possam serem plotados em um histograma,
  Globals:
    num_gaussianos : Quantidade de números aleatórios usados (Default=10.000)
    pode ser alterado globalmente usando quantidade_numeros_gaussianos(valor)
  Args:
    func (function) : função para a propagação do erro
    parametros list[Medida] : parametros da função definada acima
    hist (bool) : retornar ou não os valores calculados gaussianamente na função
    probabilidade(list) : uma lista [a,b] em que a é o começo do intervalo e b o fim

  Returns:
    Por padrão:
        Medida(media,desviopadrao)
    Se (hist=True):
        Medida(media,desviopadrao) 
        Numpy Array(valores usados para encontrar a média e o desvio padrão)
    Se (probabilidade=[a,b])
        float (probabilidade de o resultado estar entre [a,b])
'''
    #from . import num_gaussianos

    N=int(1e4)
    # importando variaveis e mensagens de erro
    if not callable(func): raise TypeError("Func precisa ser um callable")
    for parametro in parametros:
        if not isinstance(parametro,Medida): 
            raise TypeError("Todos os parametros precisam ser Medidas")          
    if not isinstance(probabilidade,list) or len(probabilidade) != 2:
        raise TypeError("Probabilidade é uma lista [a,b] em que a é o inicio e b o fim do intervalo")    
    if not isinstance(hist,bool): raise TypeError("Histograma precisar ser um booleano")
    #gerando valores
    means_parametros=np.array([parametro.nominal for parametro in parametros])
    stds_parametros=np.array([parametro.incerteza for parametro in parametros])
    aleatorios=np.random.normal(means_parametros,stds_parametros,size=(N,len(parametros)))
    vectorized_func=np.vectorize(func)
    y_samples=vectorized_func(*np.transpose(aleatorios))
    mean=np.mean(y_samples)
    std=np.std(y_samples)
    if probabilidade != [0,0]:
        a = probabilidade[0]
        b = probabilidade[1]
        condition=np.logical_and(y_samples>=a,y_samples<=b)
        chance=np.count_nonzero(condition)/len(y_samples)
        if hist==False: return chance
    if hist==True: return Medida(mean,std),y_samples
    return Medida(mean, std)

class Medida:
    def __init__(self,nominal,incerteza=0,unidade=""):
        """
        Inicializa uma instância da classe Medida com um valor nominal, incerteza e unidade.
        Valor númerico se entende qualquer objeto que possa interagir normalmente com floats,
        exemplos : int, float ,np.longdouble , np.float64...

        Parâmetros:
            - nominal: Um valor numérico que representa o valor nominal da medida.
            - incerteza: Um valor numérico que representa a incerteza associada à medida.
            - unidade: Uma string que descreve a unidade da medida.

        Raises:
            - TypeError: Se o nominal ou incerteza não puderem ser convertidos para um número.
            - TypeError: A unidade precisa ser uma string
        """
        try: float(nominal) ; self.nominal=nominal
        except: raise TypeError("Valor nominal inválido, é necessário um objeto que possa ser convertido para float")
        
        try: float(incerteza) ; self.incerteza=incerteza
        except: raise TypeError("Incerteza inválida, é necessário um objeto que possa ser convertido para float")

        if isinstance(unidade,str) and unidade:
            self.unidade=TODAS_UNIDADES[unidade]
        if isinstance(unidade,Unidade):
            self.unidade=unidade
        if not unidade: 
            self.unidade=TODAS_UNIDADES["adimensional"]

        if self.unidade.simbolo!="adimensional":
            self.si_nominal=self.nominal*self.unidade.cte_mult +self.unidade.cte_ad
            self.si_incerteza=self.incerteza*self.unidade.cte_mult
        else:
            self.si_nominal=self.nominal
            self.si_incerteza=self.incerteza
    def __str__(self):
        from numpy import log10
        from math import floor
        if self.unidade.nome=="adimensional":simbolo=""
        else:simbolo=self.unidade.simbolo
        erro=self.incerteza ; nominal=self.nominal
        potencia_erro=floor(log10(erro))
        mantissa=erro*10**(-potencia_erro)
        erro=round(mantissa) if mantissa<5 else 10
        erro=erro*10**potencia_erro

        parte_decimal_inteira=str(erro).split(".")

        if len(parte_decimal_inteira)==2:
            erro_casas_decimais=len(parte_decimal_inteira[1])
        else:
            erro_casas_decimais=0
        potencia_nominal=floor(log10(np.abs(nominal))) if nominal!=0 else 0
        nominal_str=f"{nominal*(10**-potencia_nominal):.{erro_casas_decimais+1}f}"
        erro_str=f"{erro*(10**-potencia_nominal):.{erro_casas_decimais+1}f}"
        if potencia_nominal!=0:
            return f"({nominal_str} ± {erro_str})E{potencia_nominal} {simbolo}"
        else:
            return f"({nominal_str} ± {erro_str}) {simbolo}"
    def __repr__(self) :
        if self.nominal or self.incerteza:
            return f"({self.nominal}±{self.incerteza})"
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
        if delta_nominal<=2*delta_incerteza:
            return True
        if delta_nominal>=3*delta_incerteza:
            return False
    def __gt__(self,outro):
        outro=self._torna_medida(outro)
        self._checa_dimensao(outro.unidade.simbolo)
        return self.si_nominal > outro.si_nominal
    def __ge__(self,outro):
        outro=self._torna_medida(outro)
        self._checa_dimensao(outro.unidade.simbolo)
        return self.si_nominal >= outro.si_nominal
    def __lt__(self,outro):
        outro=self._torna_medida(outro)
        self._checa_dimensao(outro.unidade.simbolo)
        return self.si_nominal < outro.si_nominal
    def __le__(self,outro):
        outro=self._torna_medida(outro)
        self._checa_dimensao(outro.unidade.simbolo)
        return self.si_nominal <= outro.si_nominal
    def __add__(self,outro):
        #Como existe solução análitica da soma entre duas gaussianas
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

