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
                result_time[0] = str(init_time)
                self.mysignal.emit("%s" % self.time_format)


class FirstTestWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.my_thread = None
        self.ui_first_test = Ui_Form()
        self.ui_first_test.setupUi(self)
        self.button_start = self.ui_first_test.pushButton_start
        self.button_stop = self.ui_first_test.pushButton_stop
        self.button_start.clicked.connect(self.on_clicked)
        self.button_stop.clicked.connect(self.on_finished)
        self.button_stop.setEnabled(False)

    def on_clicked(self):
        self.my_thread = MyThread()
        self.my_thread.started.connect(self.on_started)
        self.my_thread.finished.connect(self.on_finished)
        self.my_thread.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)
        self.my_thread.start()

    def on_started(self):
        self.ui_first_test.label_timer.setText("")
        self.button_stop.setEnabled(True)

    def on_finished(self):
        self.my_thread.stop_word = 'stop'
        self.button_stop.setEnabled(False)

    def on_change(self, s):
        self.ui_first_test.label_timer.setText(s)
        if self.my_thread.stop_word == 'stop':
            msg_box = QMessageBox()
            msg_box.setText("The document has been modified.")
            msg_box.setWindowTitle("Внимание!")
            msg_box.exec_()


if __name__ == '__main__':
    user_name = []
    result_time = ['']
    app = QApplication(sys.argv)
    login_window = FirstTestWindow()
    login_window.show()
    sys.exit(app.exec_())
