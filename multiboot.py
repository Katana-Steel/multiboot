#!/usr/bin/env python
import sys
# for pathwalk
# import os
# import menu
import fs

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
from PyQt5.QtCore import pyqtSlot


class MenuCreator(QDialog):

    @pyqtSlot()
    def scanUsb(self):
        dev = self.dev.currentData()
        parts = dev.partitions()
        if parts[0][0] == 1:
            idx = self.fs.findText(parts[0][1])
            self.fs.setCurrentIndex(idx)

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
        self.scan = QPushButton('Scan selected USB')
        self.scan.clicked.connect(self.scanUsb)
        hlay.addWidget(self.create)
        hlay.addWidget(self.scan)
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
        for f in fs.fileSystems:
            cbox.insertItem(0, str(f), f)

    def getAvailableUSBDevices(self, dev):
        for u in fs.getUSBDevices():
            dev.insertItem(0, str(u), u)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.generateUi()


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MenuCreator()
    d = w.exec_()
    sys.exit(d)
