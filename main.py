import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QInputDialog
from project import Ui_MainWindow
import sqlite3
from PyQt5.QtGui import QIcon
from main_finally import Final
from main_rules import Rules
import webbrowser
import pygame


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('si_icon.jpg'))
        self.con = sqlite3.connect("sigame.db")
        self.nickname, self.ok_pressed = QInputDialog.getText(self, "Регистрация",
                                                              "Как тебя зовут?")
        self.cur = self.con.cursor()
        if self.ok_pressed:
            if not self.cur.execute('''  
                        SELECT nick FROM nicknames
                            WHERE nick = ? ''', (self.nickname,)
                                    ).fetchall():
                self.round = 1
                self.result = 0
                self.enable_question = "0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;0,0,0,0,0"
                # вопросы на которые пользователь не отвечал
                self.cur.execute('''
                            INSERT INTO nicknames(nick) VALUES(?)
                                ''', (self.nickname,))
                self.con.commit()
                self.nick_id = self.cur.execute('''
                            SELECT id FROM nicknames
                                WHERE nick == ?
                            ''', (self.nickname,)).fetchall()[0][0]

                self.save_record = 0
                self.cur.execute('''
                            INSERT INTO nicknames_stats(record, nick_id, round, enable_question, results)
                             VALUES(?,?,?,?,?)
                        ''', (self.save_record, self.nick_id, self.round, self.enable_question, self.result))
                self.cur.execute('''UPDATE final
                                            SET score = 0''')
                self.con.commit()

                self.record_count.display(0)

            else:
                self.nick_id = self.cur.execute('''
                                            SELECT id FROM nicknames
                                                WHERE nick == ?
                                            ''', (self.nickname,)).fetchall()[0][0]
                self.save_record = self.cur.execute('''
                            SELECT record FROM nicknames_stats  
                                WHERE nick_id == ?
                        ''', (self.nick_id,)).fetchall()[0][0]
                self.round = (self.cur.execute('''
                            SELECT round FROM nicknames_stats
                                WHERE nick_id == ?
                        ''', (self.nick_id,)).fetchall())[0][0]
                self.enable_question = (self.cur.execute('''
                            SELECT enable_question FROM nicknames_stats
                                WHERE nick_id == ?
                        ''', (self.nick_id,)).fetchall())[0][0]
                self.cur.execute('''UPDATE final
                                            SET score = 0''')

                self.record_count.display(int(self.save_record))

            self.enable_question = self.enable_question.split(";")

            for i in range(len(self.enable_question)):
                self.enable_question[i] = self.enable_question[i].split(",")

            self.result = int((self.cur.execute('''
                                        SELECT results FROM nicknames_stats
                                            WHERE nick_id == ?
                                    ''', (self.nick_id,)).fetchall())[0][0])
            self.point_counter.display(self.result)

            self.topic_name()
            self.price_of_buttons()
            self.set_enable_question()
            self.theme1_1.clicked.connect(self.vopros)
            self.theme1_2.clicked.connect(self.vopros)
            self.theme1_3.clicked.connect(self.vopros)
            self.theme1_4.clicked.connect(self.vopros)
            self.theme1_5.clicked.connect(self.vopros)

            self.theme2_1.clicked.connect(self.vopros)
            self.theme2_2.clicked.connect(self.vopros)
            self.theme2_3.clicked.connect(self.vopros)
            self.theme2_4.clicked.connect(self.vopros)
            self.theme2_5.clicked.connect(self.vopros)

            self.theme3_1.clicked.connect(self.vopros)
            self.theme3_2.clicked.connect(self.vopros)
            self.theme3_3.clicked.connect(self.vopros)
            self.theme3_4.clicked.connect(self.vopros)
            self.theme3_5.clicked.connect(self.vopros)

            self.theme4_1.clicked.connect(self.vopros)
            self.theme4_2.clicked.connect(self.vopros)
            self.theme4_3.clicked.connect(self.vopros)
            self.theme4_4.clicked.connect(self.vopros)
            self.theme4_5.clicked.connect(self.vopros)

            self.theme5_1.clicked.connect(self.vopros)
            self.theme5_2.clicked.connect(self.vopros)
            self.theme5_3.clicked.connect(self.vopros)
            self.theme5_4.clicked.connect(self.vopros)
            self.theme5_5.clicked.connect(self.vopros)

            self.next_r.clicked.connect(self.next_round)
            self.next_r.hide()

            self.Show_Answer.clicked.connect(self.show_answer)
            self.Hide_Answer.clicked.connect(self.hide_answer)
            self.error.hide()
            self.rules_button.clicked.connect(self.rules)

            # self.all_qustions.buttonClicked.connect(self.vopros)

            self.download.clicked.connect(self.load_results)

            self.download_record.clicked.connect(self.load_records)

            self.cheat.clicked.connect(self.cheater)

            self.god_label.hide()

            self.god = False

        pygame.init()
        pygame.mixer.init()

    def set_enable_question(self):
        if self.enable_question[0][0] == '1':
            self.theme1_1.setEnabled(False)
        else:
            self.theme1_1.setEnabled(True)
        if self.enable_question[0][1] == '1':
            self.theme1_2.setEnabled(False)
        else:
            self.theme1_2.setEnabled(True)
        if self.enable_question[0][2] == '1':
            self.theme1_3.setEnabled(False)
        else:
            self.theme1_3.setEnabled(True)
        if self.enable_question[0][3] == '1':
            self.theme1_4.setEnabled(False)
        else:
            self.theme1_4.setEnabled(True)
        if self.enable_question[0][4] == '1':
            self.theme1_5.setEnabled(False)
        else:
            self.theme1_5.setEnabled(True)

        if self.enable_question[1][0] == '1':
            self.theme2_1.setEnabled(False)
        else:
            self.theme2_1.setEnabled(True)
        if self.enable_question[1][1] == '1':
            self.theme2_2.setEnabled(False)
        else:
            self.theme2_2.setEnabled(True)
        if self.enable_question[1][2] == '1':
            self.theme2_3.setEnabled(False)
        else:
            self.theme2_3.setEnabled(True)
        if self.enable_question[1][3] == '1':
            self.theme2_4.setEnabled(False)
        else:
            self.theme2_4.setEnabled(True)
        if self.enable_question[1][4] == '1':
            self.theme2_5.setEnabled(False)
        else:
            self.theme2_5.setEnabled(True)

        if self.enable_question[2][0] == '1':
            self.theme3_1.setEnabled(False)
        else:
            self.theme3_1.setEnabled(True)
        if self.enable_question[2][1] == '1':
            self.theme3_2.setEnabled(False)
        else:
            self.theme3_2.setEnabled(True)
        if self.enable_question[2][2] == '1':
            self.theme3_3.setEnabled(False)
        else:
            self.theme3_3.setEnabled(True)
        if self.enable_question[2][3] == '1':
            self.theme3_4.setEnabled(False)
        else:
            self.theme3_4.setEnabled(True)
        if self.enable_question[2][4] == '1':
            self.theme3_5.setEnabled(False)
        else:
            self.theme3_5.setEnabled(True)

        if self.enable_question[3][0] == '1':
            self.theme4_1.setEnabled(False)
        else:
            self.theme4_1.setEnabled(True)
        if self.enable_question[3][1] == '1':
            self.theme4_2.setEnabled(False)
        else:
            self.theme4_2.setEnabled(True)
        if self.enable_question[3][2] == '1':
            self.theme4_3.setEnabled(False)
        else:
            self.theme4_3.setEnabled(True)
        if self.enable_question[3][3] == '1':
            self.theme4_4.setEnabled(False)
        else:
            self.theme4_4.setEnabled(True)
        if self.enable_question[3][4] == '1':
            self.theme4_5.setEnabled(False)
        else:
            self.theme4_5.setEnabled(True)

        if self.enable_question[4][0] == '1':
            self.theme5_1.setEnabled(False)
        else:
            self.theme5_1.setEnabled(True)
        if self.enable_question[4][1] == '1':
            self.theme5_2.setEnabled(False)
        else:
            self.theme5_2.setEnabled(True)
        if self.enable_question[4][2] == '1':
            self.theme5_3.setEnabled(False)
        else:
            self.theme5_3.setEnabled(True)
        if self.enable_question[4][3] == '1':
            self.theme5_4.setEnabled(False)
        else:
            self.theme5_4.setEnabled(True)
        if self.enable_question[4][4] == '1':
            self.theme5_5.setEnabled(False)
        else:
            self.theme5_5.setEnabled(True)

        # self.all_qustions.buttonClicked.connect(self.vopros)

    def vopros(self):
        self.kto_otpravil = self.sender().objectName()
        # узнаем имя кнопки на которую нажали
        # И делаем ее неактивной
        self.sender().setEnabled(False)
        file = 'si_minute.mp3'
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(1)
        pygame.mixer.music.set_volume(0.2)

        self.output_of_the_question()

    def topic_name(self):  # изменяем названия тем
        if self.round < 3:
            # первая тема
            self.tema1 = self.cur.execute('''
                                        SELECT theme FROM themes
                                            WHERE theme_id == 1 AND round_id == ?
                                        ''', (self.round,)).fetchall()[0][0]
            self.theme1.setText(self.tema1)

            # вторая тема
            self.tema2 = self.cur.execute('''
                                                    SELECT theme FROM themes
                                                        WHERE theme_id == 2 AND round_id == ?
                                                    ''', (self.round,)).fetchall()[0][0]
            self.theme2.setText(self.tema2)

            # третья тема
            self.tema3 = self.cur.execute('''
                                                    SELECT theme FROM themes
                                                        WHERE theme_id == 3 AND round_id == ?
                                                    ''', (self.round,)).fetchall()[0][0]
            self.theme3.setText(self.tema3)

            # четвертая тема
            self.tema4 = self.cur.execute('''
                                                    SELECT theme FROM themes
                                                        WHERE theme_id == 4 AND round_id == ?
                                                    ''', (self.round,)).fetchall()[0][0]
            self.theme4.setText(self.tema4)

            # пятая тема
            self.tema5 = self.cur.execute('''
                                                    SELECT theme FROM themes
                                                        WHERE theme_id == 5 AND round_id == ?
                                                    ''', (self.round,)).fetchall()[0][0]
            self.theme5.setText(self.tema5)

    def output_of_the_question(self):  # создание доп окна для вывода вопроса
        question_and_price = list(self.kto_otpravil)
        theme_id = int(question_and_price[5])
        question_id = int(question_and_price[7])
        if question_id != "f":
            self.enable_question[theme_id - 1][question_id - 1] = '1'  # если пользователь выбрал вопрос,
            # то в таблице с вопросами заменяем на 1
            price = self.cur.execute('''
                SELECT price FROM questions
                                    WHERE theme_id = ? AND round_id == ? AND question_id == ?
                                ''', (theme_id, self.round, question_id)).fetchall()[0][0]

            self.price = int(price)
            question = self.cur.execute('''
                                SELECT question FROM questions
                                    WHERE price == ? AND theme_id == ? AND round_id == ?
                                ''', (self.price, theme_id, self.round)).fetchall()[0][0]

            self.correct_answer = self.cur.execute('''
                                SELECT answer FROM questions
                                    WHERE price == ? AND theme_id == ?
                                ''', (self.price, theme_id)).fetchall()[0][0]

            self.pol_answer, self.ok_pressed = QInputDialog.getText(self, "Вопрос?", question)

            if self.correct_answer == self.pol_answer:
                self.points = int(self.point_counter.value()) + self.price
                self.point_counter.display(self.points)
            elif (not self.god) and self.correct_answer != self.pol_answer:
                self.points = int(self.point_counter.value()) - self.price
                self.point_counter.display(self.points)
                file = 'si_noanswer.mp3'
                pygame.mixer.music.load(file)
                pygame.mixer.music.play(1)
                pygame.mixer.music.set_volume(0.2)
            elif self.god and self.correct_answer != self.pol_answer:
                self.points = int(self.point_counter.value()) + 0
                self.point_counter.display(self.points)
            if self.enable_question == [['1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1'],
                                        ['1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1']]:
                self.next_round()

    def show_answer(self, ):
        try:
            self.showAnswer.setText("Правильный ответ: " + str(self.correct_answer))
            self.showAnswer.show()
            yes_or_no, ok_pressed = QInputDialog.getItem(
                self, "Ответ", "Ваш ответ правильный?",
                ("ДА", "Нет"), 0, False)
            if ok_pressed:
                if yes_or_no == "ДА":
                    price = self.price
                    self.points = int(self.point_counter.value()) + 2 * price
                    self.point_counter.display(self.points)
        except:
            pass

    def hide_answer(self):
        self.showAnswer.hide()

    def load_records(self):  # сохранение данных в БД рекорда НЕЛЬЗЯ продолжить старую игру
        new_value = int(self.point_counter.value())
        if self.save_record < new_value:
            rounded = 0
            self.cur.execute('''
                    UPDATE nicknames_stats
                     SET record = ?, round = ?, results = ?
                     WHERE nick_id = ?''', (new_value, self.round, rounded, self.nick_id,))

        self.enable_question = '0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;0,0,0,0,0'
        self.cur.execute('''
                            UPDATE nicknames_stats
                             SET enable_question = ?
                             WHERE nick_id = ?''', (self.enable_question, self.nick_id,))
        self.con.commit()

    def load_results(self):
        try:
            new_value = int(self.point_counter.value())
            self.cur.execute('''
                                UPDATE nicknames_stats
                                 SET results = ?, round = ?
                                 WHERE nick_id = ?''', (new_value, self.round, self.nick_id,))
            for i in range(len(self.enable_question)):
                self.enable_question[i] = ",".join(self.enable_question[i])
            self.enable_question = ";".join(self.enable_question)
            self.cur.execute('''
                                UPDATE nicknames_stats
                                 SET enable_question = ?
                                 WHERE nick_id = ?''', (self.enable_question, self.nick_id,))
            self.con.commit()
        except:
            self.error.show()

    def next_round(self):
        self.round += 1
        if self.round == 3:
            file = 'si3_round.mp3'
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(1)
            pygame.mixer.music.set_volume(0.2)
            self.final_of_game()
        else:
            self.enable_question = [["0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0"],
                                    ["0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0"]]
            self.topic_name()
            self.price_of_buttons()
            self.set_enable_question()
            file = 'si_round.mp3'
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(1)
            pygame.mixer.music.set_volume(0.2)

    def price_of_buttons(self):
        if self.round < 3:
            button1_price = str(self.cur.execute('''
                                                SELECT price FROM questions
                                                    WHERE round_id == ? AND question_id == 1
                                                    ''', (self.round,)).fetchall()[0][0])
            self.theme1_1.setText(button1_price)
            self.theme2_1.setText(button1_price)
            self.theme3_1.setText(button1_price)
            self.theme4_1.setText(button1_price)
            self.theme5_1.setText(button1_price)

            button2_price = str(self.cur.execute('''
                                                        SELECT price FROM questions
                                                            WHERE round_id == ? AND question_id == 2
                                                            ''', (self.round,)).fetchall()[0][0])
            self.theme1_2.setText(button2_price)
            self.theme2_2.setText(button2_price)
            self.theme3_2.setText(button2_price)
            self.theme4_2.setText(button2_price)
            self.theme5_2.setText(button2_price)

            button3_price = str(self.cur.execute('''
                                                        SELECT price FROM questions
                                                            WHERE round_id == ? AND question_id == 3
                                                            ''', (self.round,)).fetchall()[0][0])
            self.theme1_3.setText(button3_price)
            self.theme2_3.setText(button3_price)
            self.theme3_3.setText(button3_price)
            self.theme4_3.setText(button3_price)
            self.theme5_3.setText(button3_price)

            button4_price = str(self.cur.execute('''
                                                        SELECT price FROM questions
                                                            WHERE round_id == ? AND question_id == 4
                                                            ''', (self.round,)).fetchall()[0][0])
            self.theme1_4.setText(button4_price)
            self.theme2_4.setText(button4_price)
            self.theme3_4.setText(button4_price)
            self.theme4_4.setText(button4_price)
            self.theme5_4.setText(button4_price)

            button5_price = str(self.cur.execute('''
                                                        SELECT price FROM questions
                                                            WHERE round_id == ? AND question_id == 5
                                                            ''', (self.round,)).fetchall()[0][0])
            self.theme1_5.setText(button5_price)
            self.theme2_5.setText(button5_price)
            self.theme3_5.setText(button5_price)
            self.theme4_5.setText(button5_price)
            self.theme5_5.setText(button5_price)

    def final_of_game(self):
        window = Final()
        window.exec()
        price = self.cur.execute('''
                                    SELECT score FROM final
                                                        WHERE id = ? 
                                                    ''', (1,)).fetchall()[0][0]
        points = int(self.point_counter.value()) + price
        self.point_counter.display(points)
        try:
            self.Hide_Answer.hide()
        except:
            pass
        try:
            self.Show_Answer.hide()
        except:
            pass
        try:
            self.showAnswer.show()
        except:
            pass
        try:
            self.showAnswer.show()
        except:
            pass
        self.showAnswer.setText("                         Поздравляю ты прошел игру! Не забудь сохраниться:)")

        file = 'finaltit.mp3'
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(1)
        pygame.mixer.music.set_volume(0.1)

    def rules(self):
        window1 = Rules()
        window1.exec()

    def cheater(self):
        self.kod, self.ok_pressed = QInputDialog.getText(self, "Чит-меню",
                                                         "Введи код")
        if self.ok_pressed:
            if self.kod == "final":
                self.final_of_game()
            elif self.kod == "points":
                self.kod, self.ok_press = QInputDialog.getText(self, "Чит-меню",
                                                               "Введи число")
                if self.ok_press:
                    self.points = int(self.point_counter.value()) + int(self.kod)
                    self.point_counter.display(self.points)
            elif self.kod == "god":
                self.god_label.show()
                self.god = True
            elif self.kod == "games":
                webbrowser.open_new('https://www.youtube.com/channel/UCvYkzPH2Dj9BJDL05LgBCsw')
            elif self.kod == "next":
                self.next_r.show()
            elif self.kod == "music":
                file = 'si2_closing.mp3'
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(file)
                pygame.mixer.music.play(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
