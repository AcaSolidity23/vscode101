

def document_it(func):
    def new_function(*args,**kwargs):
        print('Running function: ', func.__name__)
        print('Positional arguments:', args)
        print('Keyword arguments:', kwargs)
        result = func(*args, **kwargs)
        print('Result:', result)
        return result
    return new_function

@document_it
def add_ints(a, b):
    return a + b

print('Simple func:', add_ints(3, 5))
