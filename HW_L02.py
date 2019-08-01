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
    with open(filename, 'w') as f_n:
        f_n_writer = csv.writer(f_n)
        f_n_writer.writerows(get_data())
    

write_to_csv("test_cvs_write.csv")