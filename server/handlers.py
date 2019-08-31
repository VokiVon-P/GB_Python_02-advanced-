import json
import logging

from resolvers import resolve
from protocol import validate_request, make_response
from middlewares import compression_middleware


@compression_middleware
def handle_tcp_request(bytes_request):
    request = json.loads(bytes_request.decode())

    if validate_request(request):
        action = request.get('action')
        controller = resolve(action)
        if controller:
            try:
                response = controller(request)
                logging.debug(f'Client send request {request}')
            except Exception as err:
                response = response = make_response(
                    request, 500, f'Internal server error'
                )
                logging.critical(f'Exception - {err}')
        else:
            response = response = make_response(
                request, 404, f'Action {action} is not supported'
            )
            logging.error(f'Client call action with name {action}')
    else:
        response = make_response(
            request, 400, 'Wrong request'
        )
        logging.error(f'Client send wrong request {request}')

    string_response = json.dumps(response)
    return string_response.encode()