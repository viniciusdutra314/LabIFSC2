from copy import copy
from typing import get_args, get_origin


def checar_argumento(arg,nome_argumento,tipo_esperado,func_name):
   
    get_origin_result=get_origin(tipo_esperado)
    get_args_result=get_args(tipo_esperado)

    if (len(get_args_result)>1): #Unions Number | Medida
        match=False
        for arg_union in get_args_result:
            try:
                checar_argumento(arg,nome_argumento,arg_union,func_name)
                match=True
                break
            except TypeError: pass
        if not match:
            raise TypeError(f"Argumento {nome_argumento} (da função {func_name}) deve ser de um dos tipos {get_args_result}")
    elif (get_args_result): #tipos compostos np.ndarray[Number]
        #Como vamos usar sempre np.ndarray, precisamos só checar um elemento
        if not (isinstance(arg[0],get_args_result) and issubclass(type(arg),get_origin_result)):
            raise TypeError(f"Argumento {nome_argumento} (da função {func_name}) precisa ser do tipo {tipo_esperado}")
    else: #tipos simples Number
        if not (isinstance(arg, tipo_esperado) or issubclass(type(arg),tipo_esperado)):
            raise TypeError(f"Argumento {nome_argumento} (da função {func_name}) precisa ser do tipo {tipo_esperado}")

def remover_self_dentro_de_classe(annotations, args):
    args_para_analisar=copy(args)
    
    if len(args_para_analisar)>=len(annotations): args_para_analisar=args[1:] 

    return args_para_analisar, annotations

def obrigar_tipos(func):
    def wrapper(*args, **kwargs):
        args_para_analisar,annotations=remover_self_dentro_de_classe(func.__annotations__, args)
        
        #checar entrada, devido a usar zip, o return não é considerado
        for arg, (nome_argumento, tipo_esperado) in zip(args_para_analisar, annotations.items()):
            checar_argumento(arg,nome_argumento,tipo_esperado,func.__name__)
        result=func(*args, **kwargs)
        
        #checar saida
        if ('return' in annotations): 
            if (annotations['return'] is None) and (result is None):
                return result
            checar_argumento(result,'return',annotations['return'],func.__name__)
            
        return result
    wrapper.__name__ = func.__name__ #mensagens de erro bonitinhas
    return wrapper
