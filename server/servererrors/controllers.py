from protocol import make_response
from decorators import login_requeired
# from decorators import logged


#@logged('%(name)s - %(request)s')
@login_requeired
def get_server_errors(request):
    raise Exception('Custom server error')