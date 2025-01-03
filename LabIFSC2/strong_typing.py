def obrigar_tipos(func):
    def wrapper(*args, **kwargs):

        annotations = func.__annotations__
        for arg, (name, expected_type) in zip(args, annotations.items()):
            breakpoint()
            if not (isinstance(arg, expected_type) or issubclass(arg,expected_type)) :
                raise TypeError(f"Argument {name} must be of type {expected_type}")
        result = func(*args, **kwargs)
        if 'return' in annotations and not isinstance(result, annotations['return']):
            raise TypeError(f"Return value must be of type {annotations['return']}")
        return result
    return wrapper