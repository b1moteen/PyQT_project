from PyQt5.QtWidgets import *
from rules import Ui_Form
from PyQt5.QtGui import QIcon


class Rules(QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('si_icon.jpg'))
