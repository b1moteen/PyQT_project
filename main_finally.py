import sys
from PyQt5.QtWidgets import *
from final import Ui_rules_widget
import sqlite3
from PyQt5.QtGui import QIcon


class Final(QDialog, Ui_rules_widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("sigame.db")
        self.setWindowIcon(QIcon('si_icon.jpg'))
        self.cur = self.con.cursor()
        self.begin_final.clicked.connect(self.run_final)
        self.peek_question = 0
        self.theme1_f.clicked.connect(self.vopros)
        self.theme2_f.clicked.connect(self.vopros)
        self.theme3_f.clicked.connect(self.vopros)
        self.theme4_f.clicked.connect(self.vopros)
        self.theme5_f.clicked.connect(self.vopros)
        self.error.hide()

        self.theme1_f.hide()
        self.theme2_f.hide()
        self.theme3_f.hide()
        self.theme4_f.hide()
        self.theme5_f.hide()

        self.theme1.hide()
        self.theme2.hide()
        self.theme3.hide()
        self.theme4.hide()
        self.theme5.hide()
        self.points = self.cur.execute('''SELECT score FROM final WHERE id = 1''').fetchall()[0][0]

    def set_themes(self):
        self.tema1 = self.cur.execute('''
                                            SELECT theme FROM themes
                                                WHERE theme_id == 1 AND round_id == ?
                                            ''', (3,)).fetchall()[0][0]
        self.theme1.setText(self.tema1)

        self.tema2 = self.cur.execute('''
                                                    SELECT theme FROM themes
                                                        WHERE theme_id == 2 AND round_id == ?
                                                    ''', (3,)).fetchall()[0][0]
        self.theme2.setText(self.tema2)

        self.tema3 = self.cur.execute('''
                                                    SELECT theme FROM themes
                                                        WHERE theme_id == 3 AND round_id == ?
                                                    ''', (3,)).fetchall()[0][0]
        self.theme3.setText(self.tema3)

        self.tema4 = self.cur.execute('''
                                                    SELECT theme FROM themes
                                                        WHERE theme_id == 4 AND round_id == ?
                                                    ''', (3,)).fetchall()[0][0]
        self.theme4.setText(self.tema4)

        self.tema5 = self.cur.execute('''
                                                    SELECT theme FROM themes
                                                        WHERE theme_id == 5 AND round_id == ?
                                                    ''', (3,)).fetchall()[0][0]
        self.theme5.setText(self.tema5)
        # self.output_of_the_question()

    def vopros(self):
        self.kto_otpravil = self.sender().objectName()
        # узнаем имя кнопки на которую нажали
        # И делаем ее неактивной
        if self.peek_question < 3:
            self.sender().setEnabled(False)
            self.peek_question += 1
        else:
            self.question_vyvod()
            self.sender().setEnabled(False)

    def question_vyvod(self):
        question_and_price = list(self.kto_otpravil)
        theme_id = int(question_and_price[5])
        price = self.cur.execute('''
                        SELECT price FROM questions
                                            WHERE theme_id = ? AND round_id == ? AND question_id == ?
                                        ''', (theme_id, 3, theme_id)).fetchall()[0][0]
        price = int(price)
        question = self.cur.execute('''
                                        SELECT question FROM questions
                                            WHERE theme_id == ? AND round_id == ? AND question_id == ?
                                        ''', (theme_id, 3, theme_id)).fetchall()[0][0]

        self.correct_answer = self.cur.execute('''
                                        SELECT answer FROM questions
                                            WHERE price == ? AND theme_id == ? AND question_id == ?
                                        ''', (price, theme_id, theme_id)).fetchall()[0][0]

        self.pol_answer, self.ok_pressed = QInputDialog.getText(self, "Вопрос?", question)
        if self.correct_answer == self.pol_answer:
            self.points += price
        else:
            self.points -= price
        self.cur.execute('''
                            UPDATE final
                             SET score = ? WHERE id = 1''', (self.points,))
        self.con.commit()

    def run_final(self):
        self.set_themes()
        self.rule_final.hide()
        self.begin_final.hide()
        self.theme1_f.show()
        self.theme2_f.show()
        self.theme3_f.show()
        self.theme4_f.show()
        self.theme5_f.show()
        self.theme1.show()
        self.theme2.show()
        self.theme3.show()
        self.theme4.show()
        self.theme5.show()
