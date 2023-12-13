from PyQt5 import QtCore

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPixmap
import sys
from random import shuffle
import time
import sqlite3 as sql
from GUI.first_programm import Ui_Form


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.time_format = None
        self.curr_answers = None

    def run(self):
        init_time = 0
        while True:
            self.sleep(1)
            init_time += 1
            self.time_format = time.strftime("%H:%M:%S", time.gmtime(init_time))
            result_time[0] = str(init_time)
            self.mysignal.emit("%s" % self.time_format)


class FirstTestWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_first_test = Ui_Form()
        self.ui_first_test.setupUi(self)
        self.mythread = MyThread()
        self.mythread.started.connect(self.on_started)
        self.mythread.finished.connect(self.on_finished)
        self.mythread.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)
        self.button_start = self.ui_first_test.pushButton_start
        self.button_stop = self.ui_first_test.pushButton_stop
        self.button_start.clicked.connect(self.on_clicked)
        self.button_stop.clicked.connect(self.on_finished)

    def on_clicked(self):
        self.mythread.start()

    def on_started(self):
        self.ui_first_test.label_timer.setText("")

    def on_finished(self):
        QMessageBox.about(self, 'Ваш результат:', 'Тест завершен.\n{0} верных ответов из 10.'.format(
            self.right_answer
        ))
        exit()

    def on_change(self, s):
        self.ui_first_test.label_timer.setText(s)




if __name__ == '__main__':
    user_name = []
    result_time = ['']
    app = QApplication(sys.argv)
    login_window = FirstTestWindow()
    login_window.show()
    sys.exit(app.exec_())
