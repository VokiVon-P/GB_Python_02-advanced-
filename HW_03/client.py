import yaml
import json
import socket
from argparse import ArgumentParser
from datetime import datetime as dt
import jim_helper as jh


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

        # установим время
        presense_msg['time'] = dt.utcnow().timestamp()

        # подготовим данные к отправке
        msg, to_send = jh.send_json(presense_msg)
        print(f'Сообщение к отправке:\n{msg}')
        
        '''
        Отправляем данные на сервер
        '''
        sock.send(to_send)
        print(f'\nClient send data:\n{to_send}')
        '''
        Принимаем ответ сервера
        '''
        bytes_response = sock.recv(config.get('buffersize'))
        print(f'\nClient recieve data:\n{bytes_response}')

       
        try:
            msg, data = jh.recv_json(bytes_response)
            print(f'\nДанные от сервера:\n {msg} \n')
            
            if data['response'] == 200:
                print(f'Ответ сервера: OK')
                print(f'Сообщение от сервера: {data["alert"]}')
            else:
                print(f'Ответ сервера: {data["response"]}')
                print(f'Сообщение от сервера: {data["error"]}')
        except Exception as e: 
            print(f'Произошла ошибка при разборе ответа сервера: {str(e)}')
        finally:
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