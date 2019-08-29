from protocol import make_response

from decorators import logged

@logged('%(name)s - %(request)s')
def get_server_errors(request):
    raise Exception('Custom server error')