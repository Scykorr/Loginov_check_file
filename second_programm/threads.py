import os

from PyQt5 import QtCore
import time
from logging import LogFile
import shutil


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


class MyThreadCheckInputFile(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, input_address: str = None, compare_address: str = None):
        QtCore.QThread.__init__(self, parent)
        self.stop_word = None
        self.input_address = input_address
        self.compare_address = compare_address
        self.logging = LogFile()

    def run(self):
        while True:
            time.sleep(1)
            if self.stop_word == 'stop':
                break
            init_files = self.get_files_input()
            if init_files:
                for init_file in init_files:
                    self.logging.input_not_empty(init_file)
                    shutil.copyfile(f'{self.input_address}/{init_file}',
                                    f'{self.compare_address}/{init_file}')
                    os.remove(f'{self.input_address}/{init_file}')
                    self.logging.copy_file(init_file)
                    break
            else:
                self.logging.input_empty()

    def get_files_input(self):
        return os.listdir(self.input_address)


class MyThreadCompareInputFile(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, compare_address: str = None, standart_address: str = None):
        QtCore.QThread.__init__(self, parent)
        self.stop_word = None
        self.compare_address = compare_address
        self.standart_address = standart_address
        self.logging = LogFile()

    def run(self):
        while True:
            time.sleep(1)
            if self.stop_word == 'stop':
                break
            compare_files = self.get_files_compare()
            standart_files = self.get_files_standart()
            init_files = list(compare_files - standart_files)
            if init_files:
                for init_file in init_files:
                    self.logging.compare_not_empty(init_file)
                    file1 = r"{path}/{filename}".format(
                        path=self.compare_address,
                        filename=init_file,
                    )
                    file2 = r"{path}/{filename}".format(
                        path=self.standart_address,
                        filename=init_file,
                    )

                    with open(file1, 'br') as of1, open(file2, 'br') as of2:
                        l1 = of1.read()
                        l2 = of2.read()
                        full_size = len(set(enumerate(l1)))
                        f1_f2_size = len(set(enumerate(l1)) - set(enumerate(l2)))
                        percent_diff = round((f1_f2_size / full_size) * 100, 2)
                    self.logging.compare_file(init_file, f1_f2_size,  percent_diff)
                    break
            else:
                self.logging.compare_empty()

    def get_files_compare(self):
        return set(os.listdir(self.compare_address))

    def get_files_standart(self):
        return set(os.listdir(self.standart_address))
