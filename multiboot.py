#!/usr/bin/env python
import sys
# for pathwalk
# import os
# import menu

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
# from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
# from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
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
        hlay = QHBoxLayout()
        self.main.addLayout(hlay)
        hlay.addStretch()
        self.create = QPushButton('Create USB')
        hlay.addWidget(self.create)
        hlay.addStretch()
        hlay = QHBoxLayout()
        hlay.addWidget(QLabel('USB device: '))
        self.dev = QComboBox()
        self.getAvailableUSBDevices(self.dev)
        hlay.addWidget(self.dev)
        self.main.addLayout(hlay)
        hlay = QHBoxLayout()
        hlay.addWidget(QLabel('Selected filesystem:'))
        self.fs = QComboBox()
        hlay.addWidget(self.fs)
        self.main.addLayout(hlay)
        self.getAvailableFilesystems(self.fs)
        hlay = QHBoxLayout()
        hlay.addStretch()
        btn = QPushButton('add ISO File')
        hlay.addWidget(btn)
        hlay.addStretch()
        self.main.addLayout(hlay)

    def getAvailableFilesystems(self, cbox):
        # iterate over available mkfs.* programs
        cbox.insertItem(0, 'ext4')

    def getAvailableUSBDevices(self, dev):
        # insert actual code for detecting
        # usb flash storage
        dev.insertItem(0, '/dev/sdb')

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.generateUi()


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MenuCreator()
    d = w.exec_()
    sys.exit(d)
