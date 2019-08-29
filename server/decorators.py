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
    TODO: сделать независимой от порядка вызова других декораторов 
    ------пока должна быть верхней в списке декораторов

    Фиксирует обращение к декорируемой функции
    Логирует имя, аргументы и откуда была вызвана функция
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        f_name = getattr(func, '__name__', '< >')
        # довольно коряво - но работает
        f_from = sys._getframe().f_back.f_code.co_name
        
        logger.debug(f'Функция: {f_name} вызвана из функции: {f_from} с аргументами: {args} ')
        result = func(*args, **kwargs)
        return result

    return wrapper