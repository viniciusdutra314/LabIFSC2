from copy import copy
from typing import get_origin, get_args

def checar_argumento(arg,nome_argumento,tipo_esperado):
   
    get_origin_result=get_origin(tipo_esperado)
    get_args_result=get_args(tipo_esperado)

    if (len(get_args_result)>1): #Unions Number | Medida
        match=False
        for arg_union in get_args_result:
            try:
                checar_argumento(arg,nome_argumento,arg_union)
                match=True
                break
            except TypeError: pass
        if not match:
            raise TypeError(f"Argumento {nome_argumento} deve ser de um dos tipos {get_args_result}")
            
    elif (get_args_result): #tipos compostos Sequence[Number]
        #estamos supondo aqui homogeneidade de tipos, então basta checar o primeiro elemento.
        #infelizmente sequence podem ter tipos diferentes em Python, só que chegar todo a sequence
        #iria reduzir a performance para sequences grandes
        if not (isinstance(arg[0],get_args_result) and issubclass(type(arg),get_origin_result)):
            raise TypeError(f"Argumento {nome_argumento} precisa ser do tipo {tipo_esperado}")
    else: #tipos simples Number
        if not (isinstance(arg, tipo_esperado) or issubclass(type(arg),tipo_esperado)):
            raise TypeError(f"Argumento {nome_argumento} precisa ser do tipo {tipo_esperado}")

def remover_self_dentro_de_classe(annotations, args):
    args_para_analisar=copy(args)
    if 'self' in annotations: 
        del annotations['self']
        args_para_analisar=args[1:] 
    if len(args_para_analisar)>=len(annotations): args_para_analisar=args[1:] 

    return args_para_analisar, annotations

def obrigar_tipos(func):
    def wrapper(*args, **kwargs):
        args_para_analisar,annotations=remover_self_dentro_de_classe(func.__annotations__, args)
        
        #checar entrada, devido a usar zip, o return não é considerado
        for arg, (nome_argumento, tipo_esperado) in zip(args_para_analisar, annotations.items()):
            checar_argumento(arg,nome_argumento,tipo_esperado)
        result=func(*args, **kwargs)
        
        #checar saida
        if ('return' in annotations): checar_argumento(result,'return',annotations['return'])
            
        return result
    return wrapper
