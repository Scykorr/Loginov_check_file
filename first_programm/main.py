from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
import sys
from GUI.first_programm import Ui_Form
from threads import MyThreadTimer


class FirstTestWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.my_thread_timer = None
        self.ui_first_test = Ui_Form()
        self.ui_first_test.setupUi(self)
        self.ui_first_test.pushButton_start.clicked.connect(self.on_clicked)
        self.button_stop = self.ui_first_test.pushButton_stop
        self.button_stop.clicked.connect(self.on_finished)
        self.button_stop.setEnabled(False)
        self.ui_first_test.pushButton_files_folder.clicked.connect(self.choose_folder_files)
        self.ui_first_test.pushButton_diode.clicked.connect(self.choose_folder_diode)

    def on_clicked(self):
        self.my_thread_timer = MyThreadTimer()
        self.my_thread_timer.started.connect(self.on_started)
        self.my_thread_timer.finished.connect(self.on_finished)
        self.my_thread_timer.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)
        self.my_thread_timer.start()

    def on_started(self):
        self.ui_first_test.label_timer.setText("")
        self.button_stop.setEnabled(True)
        self.ui_first_test.pushButton_files_folder.setEnabled(False)
        self.ui_first_test.pushButton_diode.setEnabled(False)

    def on_finished(self):
        self.my_thread_timer.stop_word = 'stop'
        self.button_stop.setEnabled(False)
        self.ui_first_test.pushButton_files_folder.setEnabled(True)
        self.ui_first_test.pushButton_diode.setEnabled(True)

    def on_change(self, s):
        self.ui_first_test.label_timer.setText(s)
        if self.my_thread_timer.stop_word == 'stop':
            msg_box = QMessageBox()
            msg_box.setText("Процесс завершен.")
            msg_box.setWindowTitle("Внимание!")
            msg_box.exec_()

    def choose_folder_files(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.ui_first_test.lineEdit_files_folder.setText(dirlist)

    def choose_folder_diode(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.ui_first_test.lineEdit_for_diode.setText(dirlist)


if __name__ == '__main__':
    user_name = []
    result_time = ['']
    app = QApplication(sys.argv)
    login_window = FirstTestWindow()
    login_window.show()
    sys.exit(app.exec_())
