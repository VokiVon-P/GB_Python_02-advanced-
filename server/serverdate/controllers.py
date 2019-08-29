from datetime import datetime
from protocol import make_response

from decorators import logged

@logged('%(name)s - %(response)s')
def date_controller(request):
    return make_response(
        request, 200, datetime.now().timestamp()
    )