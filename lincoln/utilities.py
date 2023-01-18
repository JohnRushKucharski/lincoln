'''Basic utilities used thoughout the application'''
import typer
from rich import print

from functools import wraps

def exception_handler(exception: Exception, exit_code: int = 1):
    '''
    Creates an @exception_handler(exception, exit_code) annotation for functions.
    Based on: https://github.com/tiangolo/typer/issues/310.
    
    ex:
        @exception_handler(ZeroDivisionError, 9) #9 in abitrary here.
        def divide(numerator: float, denominator: float) -> float:
            if denominator == 0:
                raise ZeroDivisionError(f'{numerator}/{denominator} is undefined.')
            else:
                return numerator/denominator
    
    > divide(1, 0)
    1/0 is undefined.
    '''
    def decorator(f): #just says this wraps a function (I think)
        @wraps(f) # parameterizes decorator with decorated function (a closure)
        def wrapper(*args, **kwargs):
            try: # try to run funcion without exception
                return f(*args, **kwargs)
            except exception as e: # raised exception    
                print(f'[bold red]{type(e).__name__}:[/bold red] {str(e)}') # should print exception and message
                raise typer.Exit(code=exit_code)
        return wrapper
    return decorator
    
