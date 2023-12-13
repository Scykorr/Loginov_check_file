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



class FirstTestWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_first_test = Ui_Form_client_test1()
        self.ui_first_test.setupUi(self)
        self.ui_first_test.pushButton.clicked.connect(self.answer)
        self.questions = Client(ip_address_server, 7000).connect(
            'select iq_question, text_question from question')
        shuffle(self.questions)
        self.new_lst_question = self.questions[:10]
        self.variants = Client(ip_address_server, 7000).connect(
            'select id_var_answ, text_var_answ, var_answ_right, id_question from variant_answer')
        shuffle(self.variants)
        self.sorted_variants = self.sort_variants()
        self.counter_questions = 0
        self.counter_questions_result = 0
        self.right_answer = 0
        self.wrong_answer = 0
        self.student_fio = user_name[0]
        self.ui_first_test.radioButton_answer1.setChecked(True)
        self.get_questionts()
        self.mythread = MyThread()
        self.on_clicked()
        self.mythread.started.connect(self.on_started)
        self.mythread.finished.connect(self.on_finished)
        self.mythread.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)

    def on_clicked(self):
        self.mythread.start()

    def on_started(self):
        self.ui_first_test.label_timer.setText("")

    def on_finished(self):
        res_sec = 600 - int(result_time[0])
        time_format_result = time.strftime("%H:%M:%S", time.gmtime(res_sec))
        result_points = self.right_answer * 10
        Client(ip_address_server, 7000).connect(
            "update user set time='{0}', true_answer={1}, false_answer={2}, current_answer={3},"
            " result_score={5} where fio_user='{4}'".format(
                time_format_result,
                self.right_answer,
                self.wrong_answer,
                self.counter_questions_result,
                self.student_fio,
                result_points,
            ))
        QMessageBox.about(self, 'Ваш результат:', 'Тест завершен.\n{0} верных ответов из 10.'.format(
            self.right_answer
        ))
        exit()

    def on_change(self, s):
        self.ui_first_test.label_timer.setText(s)

    def answer(self):
        self.counter_questions_result += 1
        if self.ui_first_test.radioButton_answer1.isChecked() \
                and self.sorted_variants[self.counter_questions][0][2] == 1:
            self.right_answer += 1
            self.right_answer_append()
        elif self.ui_first_test.radioButton_answer2.isChecked() \
                and self.sorted_variants[self.counter_questions][1][2] == 1:
            self.right_answer += 1
            self.right_answer_append()
        elif self.ui_first_test.radioButton_answer3.isChecked() \
                and self.sorted_variants[self.counter_questions][2][2] == 1:
            self.right_answer += 1
            self.right_answer_append()
        elif self.ui_first_test.radioButton_4.isChecked() \
                and self.sorted_variants[self.counter_questions][3][2] == 1:
            self.right_answer += 1
            self.right_answer_append()
        else:
            self.wrong_answer += 1
            Client(ip_address_server, 7000).connect(
                "update user set false_answer={0}, current_answer={1} where fio_user='{2}'".format(
                    self.wrong_answer,
                    self.counter_questions_result,
                    self.student_fio,
                ))

        self.ui_first_test.radioButton_answer1.setChecked(True)
        self.ui_first_test.radioButton_answer2.setChecked(False)
        self.ui_first_test.radioButton_answer3.setChecked(False)
        self.ui_first_test.radioButton_4.setChecked(False)
        self.counter_questions += 1
        if self.counter_questions < 10:
            self.get_questionts()
        else:
            self.on_finished()
            exit()

    def right_answer_append(self):
        Client(ip_address_server, 7000).connect(
            "update user set true_answer={0}, current_answer={1} where fio_user='{2}'".format(
                self.right_answer,
                self.counter_questions_result,
                self.student_fio,
            ))

    def get_questionts(self):
        self.ui_first_test.label_img_question.clear()
        self.ui_first_test.label_img_var1.clear()
        self.ui_first_test.label_img_var2.clear()
        self.ui_first_test.label_img_var3.clear()
        self.ui_first_test.label_img_var4.clear()

        self.setWindowTitle('Вопрос №{0}'.format(
            self.counter_questions + 1,
        ))
        self.ui_first_test.plainTextEdit.setPlainText(self.new_lst_question[self.counter_questions][1])
        self.ui_first_test.radioButton_answer1.setText(self.sorted_variants[self.counter_questions][0][1])
        self.ui_first_test.radioButton_answer2.setText(self.sorted_variants[self.counter_questions][1][1])
        self.ui_first_test.radioButton_answer3.setText(self.sorted_variants[self.counter_questions][2][1])
        self.ui_first_test.radioButton_4.setText(self.sorted_variants[self.counter_questions][3][1])

        id_question = self.new_lst_question[self.counter_questions][0]
        id_var1 = self.sorted_variants[self.counter_questions][0][0]
        id_var2 = self.sorted_variants[self.counter_questions][1][0]
        id_var3 = self.sorted_variants[self.counter_questions][2][0]
        id_var4 = self.sorted_variants[self.counter_questions][3][0]

        con = sql.connect('img.db')
        cur = con.cursor()
        img_bin = cur.execute(
            'select image from img where id_question="{0}"'.format(
                id_question,
            ))
        img_bin = img_bin.fetchone()
        con.commit()
        cur.close()
        con.close()
        pix = QPixmap()
        if img_bin != None:
            if pix.loadFromData(img_bin[0], 'png'):
                self.ui_first_test.label_img_question.setPixmap(pix)

        con = sql.connect('img.db')
        cur = con.cursor()
        img_bin = cur.execute(
            'select image from img where id_variant="{0}"'.format(
                id_var1,
            ))
        img_bin = img_bin.fetchone()
        con.commit()
        cur.close()
        con.close()
        pix1 = QPixmap()
        if img_bin != None:
            if pix1.loadFromData(img_bin[0], 'png'):
                self.ui_first_test.label_img_var1.setPixmap(pix1)

        con = sql.connect('img.db')
        cur = con.cursor()
        img_bin = cur.execute(
            'select image from img where id_variant="{0}"'.format(
                id_var2,
            ))
        img_bin = img_bin.fetchone()
        con.commit()
        cur.close()
        con.close()
        pix2 = QPixmap()
        if img_bin != None:
            if pix2.loadFromData(img_bin[0], 'png'):
                self.ui_first_test.label_img_var2.setPixmap(pix2)

        con = sql.connect('img.db')
        cur = con.cursor()
        img_bin = cur.execute(
            'select image from img where id_variant="{0}"'.format(
                id_var3,
            ))
        img_bin = img_bin.fetchone()
        con.commit()
        cur.close()
        con.close()
        pix3 = QPixmap()
        if img_bin != None:
            if pix3.loadFromData(img_bin[0], 'png'):
                self.ui_first_test.label_img_var3.setPixmap(pix3)

        con = sql.connect('img.db')
        cur = con.cursor()
        img_bin = cur.execute(
            'select image from img where id_variant="{0}"'.format(
                id_var4,
            ))
        img_bin = img_bin.fetchone()
        con.commit()
        cur.close()
        con.close()
        pix4 = QPixmap()
        if img_bin != None:
            if pix4.loadFromData(img_bin[0], 'png'):
                self.ui_first_test.label_img_var4.setPixmap(pix4)


    def sort_variants(self):
        new_list = [[] for _ in range(10)]
        counter = 0
        for question in self.new_lst_question:
            for var in self.variants:
                if question[0] == var[3]:
                    new_list[counter].append(var)
            counter += 1
        return new_list
