import yaml
import json
import socket
from argparse import ArgumentParser
from pprint import pprint


'''
Описываем конфигурацию по умолчанию
'''
config = {
    'host': '127.0.0.1',
    'port': 8000,
    'buffersize': 1024
}

'''
Создаём объект парсера аргументов командной строки
'''
parser = ArgumentParser()

'''
Добавляем аргументы для парсинга
Перечень допустимых аргументов конфигурации аргумента командной строки можно найти здесь:
https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
'''
parser.add_argument(
    '-c', '--config', type=str, required=False,
    help='Sets config file path'
)

'''
Создаем пространство имён args на основе аргументов командной строки
https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args
'''
args = parser.parse_args()
pprint(config)
'''
Обновляем конфигурацию на основе словаря
Подробнее о словарях python можно узнать здесь:
https://docs.python.org/3/tutorial/datastructures.html#dictionaries
'''
if args.config:
    with open(args.config) as file:
        file_config = yaml.safe_load(file)
        config.update(file_config or {})

pprint(config)

host, port = config.get('host'), config.get('port')

'''
Код в теле данной конструкции будет выполнен только в случае запуска данного модуля
python server.py [-c]
'''
if __name__ == '__main__':
    try:
        '''
        Создаём сокет
        https://docs.python.org/3/library/socket.html#socket.socket
        '''
        sock = socket.socket()
        '''
        Связываем сервер с его IP
        Если адрес уже занят метод bind вызовет ошибку
        '''
        sock.bind((host, port))
        '''
        Переводим сокет в режим ожидания 
        '''
        sock.listen(5)

        print(f'Server started with {host}:{port}')

        while True:
            '''
            Устанавливаем подключение с клиентом
            '''
            client, address = sock.accept()
            client_host, client_port = address
            print(f'Client was detected {client_host}:{client_port}')

            '''
            Принимаем запрос клиента
            '''
            bytes_request = client.recv(config.get('buffersize'))
            msg = bytes_request.decode('utf-8')
            print(f'Client send message {msg}')
            
            '''
            Отправляем ответ клиенту
            '''
            client.send(bytes_request)
            '''
            Закрываем клиентский сокет
            '''
            client.close()
    except KeyboardInterrupt:
        '''
        В случае нажатия сочетания клавиш Ctrl+C(Ctrl+Backspace на windows)
        обрабатываем завершение работы сервера
        '''
        print('Server shutdown')