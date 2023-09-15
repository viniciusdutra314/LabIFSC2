import numpy as np
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

        if isinstance(unidade,str): self.unidade=unidade
        else: raise TypeError("Unidade precisa ser uma string")
    def __eq__(self,outro):
        delta_nominal=abs(self.nominal - outro.nominal)
        delta_incerteza=abs(self.incerteza + outro.incerteza)
        return delta_nominal<=2*delta_incerteza
    def __str__(self):
        ...
def montecarlo(func : callable, *parametros : list[Medida]  , 
               hist : bool=False,probabilidade : list[float] =[0,0]) -> Medida:
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


