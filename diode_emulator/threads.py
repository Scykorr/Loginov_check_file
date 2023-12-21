import os

from PyQt5 import QtCore
import time
import shutil
import datetime


class LogFile:
    def diode_empty(self):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файла в папке для отправки не оказалось {datetime.datetime.now()}\n')

    def diode_not_empty(self, init_file):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файл {init_file} в папке для отправки {datetime.datetime.now()}\n')

    def copy_diode_folder(self, init_file):
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(
                f'Файл {init_file} успешно скопирован в папку для отправки {datetime.datetime.now()}\n')


class MyThreadTimer(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, result_time=None):
        QtCore.QThread.__init__(self, parent)
        if result_time is None:
            result_time = ['']
        self.result_time = result_time
        self.time_format = None
        self.curr_answers = None
        self.stop_word = None

    def run(self):
        init_time = 0
        while True:
            if self.stop_word == 'stop':
                break
            else:
                self.sleep(1)
                init_time += 1
                self.time_format = time.strftime("%H:%M:%S", time.gmtime(init_time))
                self.result_time[0] = str(init_time)
                self.mysignal.emit("%s" % self.time_format)


class MyThreadCheckFile(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, files_address: str = None, diode_address: str = None):
        QtCore.QThread.__init__(self, parent)
        self.stop_word = None
        self.input_address = files_address
        self.output_address = diode_address
        self.logging = LogFile()

    def run(self):
        while True:
            time.sleep(2)
            init_files = self.get_file_list_folder_with_files()
            if init_files:
                for init_file in init_files:
                    while True:
                        time.sleep(1)
                        diode_files = self.get_file_list_folder_diode()
                        if self.stop_word == 'stop':
                            break
                        elif not diode_files:
                            self.logging.diode_empty()
                            shutil.copyfile(f'{self.input_address}/{init_file}', f'{self.output_address}/{init_file}')
                            self.logging.copy_diode_folder(init_file)
                            os.remove(f'{self.input_address}/{init_file}')
                            break
                        elif diode_files:
                            self.logging.diode_not_empty(init_file)

    def get_file_list_folder_with_files(self):
        return os.listdir(self.input_address)

    def get_file_list_folder_diode(self):
        return os.listdir(self.output_address)
