from protocol import make_response

from decorators import logged
from decorators import log_call_info

"""
Добавил декоратор для теста
"""

@log_call_info
@logged('%(name)s - %(response)s')
def echo_controller(request):
    data = request.get('data')
    return make_response(request, 200, data)