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
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
# from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
# from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi


class MenuCreator(QDialog):

    @pyqtSlot()
    def scanUsb(self):
        dev = self.dev.currentData()
        if dev is not None:
            parts = dev.partitions()
            if parts[0][0] == 1:
                idx = self.fs.findText(parts[0][1])
                self.fs.setCurrentIndex(idx)

    @pyqtSlot()
    @pyqtSlot(int)
    def updateUsb(self, idx=None):
        self.getAvailableUSBDevices(self.dev)

    def generateUi(self):
        self.loop = QTimer(self)
        self.loop.setInterval(500)
        self.loop.timeout.connect(self.updateUsb)
#        self.ui = loadUi("ui/main.ui")
#        self.main = QVBoxLayout(self)
#        self.main.addWidget(self.ui)
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
        self.dev.activated.connect(self.updateUsb)
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
        self.btn = QPushButton('add ISO File')
        hlay.addWidget(self.btn)
        hlay.addStretch()
        self.main.addLayout(hlay)
        hlay = QHBoxLayout()
        hlay.addStretch()
        self.img_list = QListWidget()
        hlay.addWidget(self.img_list)
        hlay.addStretch()
        self.main.addLayout(hlay)
        self.loop.start()

    def getAvailableFilesystems(self, cbox):
        for f in fs.fileSystems:
            cbox.insertItem(0, str(f), f)

    def getAvailableUSBDevices(self, dev):
        txt = dev.currentText()
        dev.clear()
        for u in fs.getUSBDevices():
            dev.insertItem(0, str(u), u)
        if dev.count() < 1:
            dev.insertItem(0,u'', None)
        else:
            # check if our currently selected device is still there
            idx = dev.findText(txt)
            if idx != -1:
                dev.setCurrentIndex(idx)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.generateUi()


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MenuCreator()
    d = w.exec_()
    sys.exit(d)
