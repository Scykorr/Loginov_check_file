import datetime


class LogFile:
    def input_empty(self):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файла в папке получения не оказалось {datetime.datetime.now()}\n')

    def input_not_empty(self, init_file):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файл {init_file} в папке получения {datetime.datetime.now()}\n')

    def copy_file(self, init_file):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файл {init_file} успешно перемещен в папку для сравнения {datetime.datetime.now()}\n')

    def compare_file(self, init_file):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файл {init_file} успешно прошел процесс сравнения {datetime.datetime.now()}\n')

    def compare_empty(self):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файла в папке сравнения не оказалось {datetime.datetime.now()}\n')

    def compare_not_empty(self, init_file):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файл {init_file} в папке сравнения {datetime.datetime.now()}\n')
