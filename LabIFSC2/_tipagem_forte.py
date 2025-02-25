from collections.abc import Callable
from copy import copy
from functools import wraps
from types import UnionType
from typing import Any, get_args, get_origin

import numpy as np


def checar_argumento(arg:Any,nome_argumento:str,tipo_esperado:Any,
                     func_name:str)->None:
   
    if isinstance(tipo_esperado, str):
        return None
    get_origin_result=get_origin(tipo_esperado)
    get_args_result=get_args(tipo_esperado)

    if (get_origin_result is UnionType): #Unions Number | Medida
        match=False
        for arg_union in get_args_result:
            try:
                checar_argumento(arg,nome_argumento,arg_union,func_name)
                match=True
                break
            except TypeError: pass
        if not match:
            raise TypeError(f"Argumento {nome_argumento} (da função {func_name}) deve ser de um dos tipos {get_args_result} \
e não {type(arg)}")
    
    else: #tipos simples 
        if not (isinstance(arg, tipo_esperado) or issubclass(type(arg),tipo_esperado)):
            raise TypeError(f"Argumento {nome_argumento} (da função {func_name}) precisa ser do tipo {tipo_esperado} \
 e não {type(arg)}")

def remover_self_dentro_de_classe(annotations:dict[str,Any], args:tuple[Any,...])->tuple[tuple[Any,...],dict[str,Any]]:
    args_para_analisar=copy(args)
    
    if len(args_para_analisar)>=len(annotations): 
        args_para_analisar=args[1:] 

    return args_para_analisar, annotations

def obrigar_tipos(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
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
    return wrapper
