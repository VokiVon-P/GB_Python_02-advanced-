import re
import csv


def get_data():

    patterns = [re.compile("(Изготовитель системы:).*"),
                re.compile("(Название ОС:).*"),
                re.compile("(Код продукта:).*"),
                re.compile("(Тип системы:).*")]

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data =  [ headers ]
    f_names = ["data/info_1.txt", "data/info_2.txt", "data/info_3.txt"]


    def read_one_file(filename):
        with open(filename, 'rt') as myfile:
            try:
                data = myfile.read()
                tmp_list = []
                for ptrn in patterns:
                    mr = ptrn.search(data)
                    info = mr.group().split(":")[1].strip()
                    tmp_list.append(info)

                main_data.append(tmp_list)

            except Exception as err:
                print(f"Ошибка чтения файла {filename}\n", err)


    for fname in f_names:
        read_one_file(fname)

    print(main_data)
    return main_data


def write_to_csv(filename):
    try:
        with open(filename, 'w') as f_n:
            f_n_writer = csv.writer(f_n)
            f_n_writer.writerows(get_data())

    except Exception as err:
                print(f"Ошибка записи файла {filename}\n", err)

# TODO расскомментироваь
#  write_to_csv("test_cvs_write.csv")

"""
Задание на закрепление знаний по модулю json. 
Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. 
Для этого:
Создать функцию write_order_to_json(), в которую передается 
5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date). 
Функция должна предусматривать запись данных в виде словаря в файл orders.json. 
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""

import json
import uuid
import datetime


def write_order_to_json(item, quantity, price, buyer, date):

    _fname = "data/orders.json"
    # читаем текущий файл заказов
    def read_orders():

        filename = _fname
        try:
            with open(filename) as f_n:
                objs = json.load(f_n)
                return objs
                
        except Exception as err:
                print(f"Ошибка чтения файла {filename}\n", err)


    def write_orders(orders):

        filename = _fname
        try:
            with open(_fname, 'w') as f_n:
                json.dump(orders, f_n, indent=4) #sort_keys=True, 

        except Exception as err:
                print(f"Ошибка записи файла {filename}\n", err)                    


    def make_order(item, quantity, price, buyer, date):
        # создаем словарь для записи 
        order_item = {'item' : item, 'quantity' : quantity, 'price' : price, 'buyer' : buyer, 'date' : date}
        # order = {"order_id":uuid.uuid1(), 'items' : order_item}
        return order_item


    main_json_dict = read_orders()
    orders = main_json_dict['orders']
    order = make_order(item, quantity, price, buyer, date)
    orders.append({str(uuid.uuid1()): order})
    write_orders(main_json_dict)


# запись в JSON    
# TODO расскомментироваь
# write_order_to_json("Лопата", 10, 100, "Петрович", str(datetime.date.today())) 