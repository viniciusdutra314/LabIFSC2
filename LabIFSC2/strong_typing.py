def obrigar_tipos(in_class_function : bool =False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            annotations = func.__annotations__
            result = func(*args, **kwargs)
            if (in_class_function):
                args=args[1:]
            for arg, (name, expected_type) in zip(args, annotations.items()):
                if not (isinstance(arg, expected_type) or issubclass(expected_type, type(arg))):
                    raise TypeError(f"Argument {name} must be of type {expected_type}")
            if 'return' in annotations and not isinstance(result, annotations['return']):
                raise TypeError(f"Return value must be of type {annotations['return']}")
            return result
        return wrapper
    return decorator
