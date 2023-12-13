class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.time_format = None
        self.curr_answers = None

    def run(self):
        for i in range(600, -1, -1):
            self.sleep(1)
            self.time_format = time.strftime("%H:%M:%S", time.gmtime(i))
            result_time[0] = str(i)
            self.mysignal.emit("Осталось времени = %s" % self.time_format)