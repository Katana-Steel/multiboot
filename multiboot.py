#!/usr/bin/env python
import sys
# import menu

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
# from PyQt5.QtWidgets import QLineEdit
# from PyQt5.QtWidgets import QLabel
# from PyQt5.QtWidgets import QPushButton
# from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
# from PyQt5.QtWidgets import QHBoxLayout
# from PyQt5.QtGui import QIntValidator
# from PyQt5.QtCore import pyqtSlot


class MenuCreator(QDialog):

    def generateUi(self):
        self.setWindowTitle('Bootmenu creator')
        s = self.size()
        s.setWidth(300)
        s.setHeight(0)
        self.setMinimumSize(s)
        self.main = QVBoxLayout(self)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.generateUi()


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MenuCreator()
    d = w.exec_()
    sys.exit(d)
