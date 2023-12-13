import os

from PyQt5 import QtCore
import time
import datetime


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
        self.files_address = files_address
        self.diode_address = diode_address

    def run(self):
        init_time = 0
        init_files = self.get_file_list_folder_with_files()
        if init_files:
            for init_file in init_files:
                while True:
                    time.sleep(1)
                    diode_files = self.get_file_list_folder_diode()
                    if self.stop_word == 'stop':
                        break
                    elif not diode_files:
                        with open('log.txt', 'a', encoding='UTF-8') as file:
                            file.write(
                                f'Файла в папке для отправки не оказалось {datetime.datetime.now(datetime.UTC)}\n')
                    elif not diode_files:
                        with open('log.txt', 'a', encoding='UTF-8') as file:
                            file.write(
                                f'Файл {init_file} в папке для отправки {datetime.datetime.now(datetime.UTC)}\n')

    def get_file_list_folder_with_files(self):
        return os.listdir(self.files_address)

    def get_file_list_folder_diode(self):
        return os.listdir(self.diode_address)
