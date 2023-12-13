import datetime


class LogFile:
    def diode_empty(self):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файла в папке для отправки не оказалось {datetime.datetime.now(datetime.UTC)}\n')

    def diode_not_empty(self, init_file):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файл {init_file} в папке для отправки {datetime.datetime.now(datetime.UTC)}\n')

    def copy_diode_folder(self, init_file):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файл {init_file} успешно скопирован в папку для отправки {datetime.datetime.now(datetime.UTC)}\n')
