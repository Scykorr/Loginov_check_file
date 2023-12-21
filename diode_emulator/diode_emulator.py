from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
import sys
from GUI.diode import Ui_Form
from threads import MyThreadTimer, MyThreadCheckFile


class FirstTestWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.my_thread_check_file = None
        self.my_thread_timer = None
        self.ui_first_test = Ui_Form()
        self.ui_first_test.setupUi(self)
        self.ui_first_test.pushButton_start.clicked.connect(self.on_clicked)
        self.button_stop = self.ui_first_test.pushButton_stop
        self.button_stop.clicked.connect(self.on_finished_timer)
        self.button_stop.setEnabled(False)
        self.ui_first_test.pushButton_files_folder.clicked.connect(self.choose_folder_files)
        self.ui_first_test.pushButton_diode.clicked.connect(self.choose_folder_diode)
        self.setWindowTitle('Диод')

    def on_clicked(self):
        if self.ui_first_test.lineEdit_files_folder.text() != '' or self.ui_first_test.lineEdit_for_diode.text() != '':
            self.button_stop.setEnabled(True)
            self.ui_first_test.pushButton_start.setEnabled(False)
            self.ui_first_test.pushButton_files_folder.setEnabled(False)
            self.ui_first_test.pushButton_diode.setEnabled(False)
            self.my_thread_timer = MyThreadTimer()
            self.my_thread_timer.started.connect(self.on_started_timer)
            self.my_thread_timer.finished.connect(self.on_finished_timer)
            self.my_thread_timer.mysignal.connect(self.on_change_timer, QtCore.Qt.QueuedConnection)
            self.my_thread_timer.start()
            self.my_thread_check_file = MyThreadCheckFile(files_address=self.ui_first_test.lineEdit_files_folder.text(),
                                                          diode_address=self.ui_first_test.lineEdit_for_diode.text())
            self.my_thread_check_file.started.connect(self.on_started_check_file)
            self.my_thread_check_file.finished.connect(self.on_finished_timer)
            self.my_thread_check_file.start()
        else:
            msg_box = QMessageBox()
            msg_box.setText("Поля не заполнены!")
            msg_box.setWindowTitle("Внимание!")
            msg_box.exec_()

    def on_started_timer(self):
        self.ui_first_test.label_timer.setText("")

    def on_finished_timer(self):
        self.my_thread_timer.stop_word = 'stop'
        self.button_stop.setEnabled(False)
        self.ui_first_test.pushButton_files_folder.setEnabled(True)
        self.ui_first_test.pushButton_diode.setEnabled(True)
        self.ui_first_test.pushButton_start.setEnabled(True)

    def on_change_timer(self, s):
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

    def on_started_check_file(self):
        pass


if __name__ == '__main__':
    user_name = []
    result_time = ['']
    app = QApplication(sys.argv)
    login_window = FirstTestWindow()
    login_window.show()
    sys.exit(app.exec_())
