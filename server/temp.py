from functools import wraps

import sys 


def vok(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(getattr(func, '__name__', '!!!'))
        print('%(args)s', args) 
        print('%'*50)
        print(sys._getframe().f_back.f_code.co_name) 
        result = func(*args, **kwargs)
        return result
   
    return wrapper


def show_attr(func):
    print('='*50)
    for key in dir(func):
        print(f'{key} = {getattr(func, key, "NNN")}')
    print('='*50)


@vok
def test_decor():
    print(f'Вызвана функция : {test_decor.__name__}')
    #show_attr(test_decor)
    print(f'Вызвана функция : {test_decor.__name__}')
     


""" def print_caller_name(stack_size = 3): 
    def wrapper (fn): 
        def internal (* args, ** kwargs): 
            stack = inspect.stack() 
            modules = [(index, inspect.getmodule(stack[index][0]))]
            #для индекса в обратном (диапазон (1, stack_size))] 
            module_name_lengths = [len(module.__ name__)]
            s  = '{index: & gt; 5}: {module: ^% i}: {name}'% (max (module_name_lengths) + 4) 
            callers = ['', s.format (index = 'level', module = '  module ', name =' name '),' - '* 50] 
            callers.append (s.format (index = index, module = module .__ name__, name = stack [index] [3])) 
            callers.append (s.format (index = 0, module = fn .__ module__, name = fn .__ name__)) 
            callers.append ('') print ('\n'.join (вызывающие)) 
            fn (* args  , ** kwargs) 
        return internal 
    return wrapper  
 """



def test():
    print("- до вызова тестовой функции!")
    test_decor()
    print("- после вызова тестовой функции!")



test()