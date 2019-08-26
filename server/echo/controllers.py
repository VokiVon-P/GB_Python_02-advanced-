from protocol import make_response

from decorators import logged
from decorators import vok


#@logged('%(name)s - %(response)s')
@vok
def echo_controller(request):
    data = request.get('data')
    return make_response(request, 200, data)