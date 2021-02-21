import yaml
import json
import socket
from argparse import ArgumentParser
from pprint import pprint
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

ok_msg = {
    "response": 200,
    "alert":"OK"
}

err_msg = {
    "response": 400,
    "error": u"неправильный запрос/JSON-объект"
}

presense_msg = 'presence'


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

'''
Обновляем конфигурацию на основе словаря
Подробнее о словарях python можно узнать здесь:
https://docs.python.org/3/tutorial/datastructures.html#dictionaries
'''
if args.config:
    with open(args.config) as file:
        file_config = yaml.safe_load(file)
        config.update(file_config or {})

       
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

            # Разбираем что пришло от клиента
            try:
                msg, data = jh.recv_json(bytes_request)
                print(f'Client send message:\n{msg}')
                
                if data["action"] == presense_msg:
                    user_name = data.get('user').get('account_name')
                    ok_msg['alert'] = f"Привет тебе {user_name}"

                    msg, bytes_send  = jh.send_json(ok_msg)
                    print(f'Server send message to client {user_name}:\n{msg}')
                
                else:
                    raise Exception(f'Ожидалась команда: {presense_msg}')

            except Exception as e:
                err_msg['error'] += f" [{str(e)}]" 
                msg, bytes_send  = jh.send_json(err_msg)
                print(f'Server send message to client:\n{msg}')
                
            finally:
                '''
                Отправляем ответ клиенту
                '''
                client.send(bytes_send)
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



        