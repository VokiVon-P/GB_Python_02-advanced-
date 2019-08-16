import yaml
import json
import socket
from datetime import datetime
from argparse import ArgumentParser


def make_request(action, data):
    return {
        'action': action,
        'data': data,
        'time': datetime.now().timestamp()
    }


config = {
    'host': '127.0.0.1',
    'port': 8000,
    'buffersize': 1024
}

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False,
    help='Sets config file path'
)
parser.add_argument(
    '-ht', '--host', type=str, required=False,
    help='Sets server host'
)
parser.add_argument(
    '-p', '--port', type=int, required=False,
    help='Sets server port'
)

args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        file_config = yaml.safe_load(file)
        config.update(file_config or {})

if args.host:
    config['host'] = args.host

if args.port:
    config['port'] = args.port

if __name__ == '__main__':
    try:
        sock = socket.socket()
        sock.connect((config.get('host'), config.get('port')))

        print('Client was started')

        action = input('Enter action: ')
        data = input('Enter data: ')

        request = make_request(action, data)

        string_request = json.dumps(request)

        sock.send(string_request.encode())
        print('Client send data')

        bytes_response = sock.recv(config.get('buffersize'))
        print(bytes_response.decode())
        sock.close()
    except KeyboardInterrupt:
        print('Client shutdown')