import json
'''
Вспомогательные функции для перевода JSON для сетевого взаимодействия
Версия 0 - тестовая без проверок и эксепшн
'''

# функция для подготовки к отправке JSON
def send_json(obj:dict)-> tuple:
    msg = json.dumps(obj, ensure_ascii=False, indent=4)
    bytes_send = msg.encode('utf-8')
    return (msg, bytes_send)


# функция для разбора ответа в JSON
def recv_json(arr:bytearray)-> tuple:
    msg = msg = arr.decode('utf-8')
    data = json.loads(msg, parse_float=float)
    return (msg, data)



if __name__ == "__main__":
    print("Не запускайте меня на исполнение!")
    pass

