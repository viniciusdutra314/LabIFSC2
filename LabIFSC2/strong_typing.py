from copy import copy
from typing import get_origin, get_args

def obrigar_tipos(in_class_function : bool =False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            annotations = func.__annotations__
            args_originais=copy(args)
            if (in_class_function): args=args[1:] #pula self
            
            #input
            for arg, (name, expected_type) in zip(args, annotations.items()):
                original_type=get_origin(expected_type)
                arg_type=get_args(expected_type)
                if (arg_type):
                   if not (isinstance(arg[0],arg_type) or issubclass(original_type, type(arg))):
                        raise TypeError(f"Argument {name} must be of type {expected_type}")
                else:
                    if not (isinstance(arg, expected_type) or issubclass(expected_type, type(arg))):
                        raise TypeError(f"Argument {name} must be of type {expected_type}")
            result=func(*args_originais, **kwargs)
             
            #return
            if ('return' in annotations):
                if (get_args(annotations['return'])): 
                    expected_return_type=get_origin(annotations['return'])
                    expected_return_args=get_args(annotations['return'])
                    if not (isinstance(result,expected_return_type) or isinstance(result[0],expected_return_args)) :
                        raise TypeError(f"Return value must be of type {annotations['return']}")
                else:
                    if not isinstance(result,annotations['return']):
                        raise TypeError(f"Return value must be of type {annotations['return']}")
                
            return result
        return wrapper
    return decorator
