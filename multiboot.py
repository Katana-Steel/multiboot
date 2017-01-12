#!/usr/bin/env python
import sys
# for pathwalk
# import os
# import menu
import fs

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QComboBox
# from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QPushButton
# from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
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

    def LoadUi(self):
        self.setWindowTitle('Bootmenu creator')
        s = self.size()
        s.setWidth(300)
        s.setHeight(0)
        self.setMinimumSize(s)
        self.ui = loadUi("ui/main.ui")
        self.main = QVBoxLayout(self)
        self.main.addWidget(self.ui)
        self.fs = self.ui.findChild(QComboBox, 'fileSystem')
        self.getAvailableFilesystems(self.fs)
        self.dev = self.ui.findChild(QComboBox, 'devices')
        self.getAvailableUSBDevices(self.dev)
        self.create = self.ui.findChild(QPushButton, 'createUsb')
        self.scan = self.ui.findChild(QPushButton, 'scanDevice')
        self.scan.clicked.connect(self.scanUsb)

        self.loop = QTimer(self)
        self.loop.setInterval(500)
        self.loop.timeout.connect(self.updateUsb)
        self.loop.start()

    def getAvailableFilesystems(self, cbox):
        for f in fs.fileSystems:
            cbox.insertItem(0, str(f), f)

    def getAvailableUSBDevices(self, dev):
        txt = dev.currentText()
        usb_lst = fs.getUSBDevices()
        dev.clear()
        for u in usb_lst:
            dev.insertItem(0, str(u), u)
        if dev.count() < 1:
            dev.insertItem(0, u'', None)
        else:
            # check if our currently selected device is still there
            idx = dev.findText(txt)
            if idx != -1:
                dev.setCurrentIndex(idx)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.LoadUi()


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MenuCreator()
    d = w.exec_()
    sys.exit(d)
