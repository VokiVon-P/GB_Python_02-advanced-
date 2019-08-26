import logging
from functools import wraps

import sys 

logger = logging.getLogger('server.decorators')


def logged(log_format):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            response = func(request)
            logger.debug(log_format % {'name': func.__name__, 'requst': request, 'response': response})
            return response
        return wrapper
    return decorator





def log_call_info(func):
    """
    TODO:
    первая версия - дополнить 
    Фиксирует обращение к декорируемой функции
    Логирут имя и аргументы
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(getattr(func, '__name__', '< >'))
        print('%(args)s', args) 
        print('%'*50)
        # print(sys._getframe().f_back.f_code.co_name) 
        result = func(*args, **kwargs)
        return result
   
    return wrapper