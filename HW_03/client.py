import yaml
import json
import socket
from argparse import ArgumentParser
from datetime import datetime as dt


'''
Описываем конфигурацию по умолчанию
'''
config = {
    'host': '127.0.0.1',
    'port': 8000,
    'buffersize': 1024
}

presense_msg = {
    "action": "presence",
    "time": "",
    "type": "status",
    "user": {
                "account_name": "Voki-001",
                "status": u"Привет, я здесь!!!"
            }
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
parser.add_argument(
    '-ht', '--host', type=str, required=False,
    help='Sets server host'
)
parser.add_argument(
    '-p', '--port', type=int, required=False,
    help='Sets server port'
)

'''
Создаем пространство имён args на основе аргументов командной строки
https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args
'''
args = parser.parse_args()

'''
Обновляем конфигурацию на основе словаря
Подробнее о словарях python можно узнать здесь:
https://docs.python.org/3/tutorial/datastructures.html#dictionaries
'''
if args.config:
    with open(args.config) as file:
        file_config = yaml.safe_load(file)
        config.update(file_config or {})

if args.host:
    config['host'] = args.host

if args.port:
    config['port'] = args.port

'''
Код в теле данной конструкции будет выполнен только в случае запуска данного модуля
python client.py [-c] [-p] [-ht]
'''
if __name__ == '__main__':
    try:
        '''
        Создаём сокет
        https://docs.python.org/3/library/socket.html#socket.socket
        '''
        sock = socket.socket()
        '''
        Подключаемся к серверу по его IP
        Если сервер не запущен метод connect вызовет ошибку
        '''
        sock.connect((config.get('host'), config.get('port')))

        print('Client was started')

        #

        presense_msg['time'] = dt.utcnow().timestamp()
        data = json.dumps(presense_msg, ensure_ascii=False, indent=4)
        print(f'Данные к отправке:\n{data}')
        
        '''
        Отправляем данные на сервер
        '''
        to_send = data.encode('utf-8')
        sock.send(to_send)
        print(f'Client send data:\n{to_send}')
        '''
        Принимаем ответ сервера
        '''
        bytes_response = sock.recv(config.get('buffersize'))
        print(f'Client recieve data:\n{bytes_response}\n')

        print(bytes_response.decode('utf-8'))
        '''
        Закрываем сокет
        '''
        sock.close()
        
    except KeyboardInterrupt:
        '''
        В случае нажатия сочетания клавиш Ctrl+C(Ctrl+Backspace на windows)
        обрабатываем завершение работы клиента
        '''
        print('Client shutdown')