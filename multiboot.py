#!/usr/bin/env python
import sys
# for pathwalk
# import os
# import menu
import fs

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
# from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi


class IsoDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.isos = ['gnome debian 9', 'xfce debian 9']
        self.loadUi()

    def loadUi(self):
        self.setWindowTitle("Pick your ISO")
        layout = QVBoxLayout(self)
        ui = loadUi("ui/iso.ui")
        self.resize(ui.size())
        layout.addWidget(ui)
        model = QStringListModel(ui)
        view = ui.findChild(QListView, 'isoList')
        model.setStringList(self.isos)
        view.setModel(model)


class MenuCreator(QDialog):

    @pyqtSlot()
    def aboutDialog(self):
        about = """
Multiboot:\na tool to create grub2 boot menu for booting multiple different \
ISO images\nCopyright (C) 2017  Rene Kjellerup aka Katana Steel

This program is free software: you can redistribute it and/or modify \
it under the terms of the GNU General Public License as published by \
the Free Software Foundation, either version 3 of the License, or \
(at your option) any later version.

This program is distributed in the hope that it will be useful, \
but WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the \
GNU General Public License for more details.

You should have received a copy of the GNU General Public License \
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
        QMessageBox(QMessageBox.Information, 'About Multiboot', about).exec_()

    @pyqtSlot()
    def addIsoUi(self):
        iso = IsoDialog(self)
        iso.exec_()

    @pyqtSlot()
    def scanUsb(self):
        dev = self.dev.currentData()
        if dev is not None:
            parts = dev.partitions()
            if parts[0][0] == '1':
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
        about = self.ui.findChild(QPushButton, 'about')
        about.clicked.connect(self.aboutDialog)
        self.fs = self.ui.findChild(QComboBox, 'fileSystem')
        self.getAvailableFilesystems(self.fs)
        self.dev = self.ui.findChild(QComboBox, 'devices')
        self.getAvailableUSBDevices(self.dev)
        self.create = self.ui.findChild(QPushButton, 'createUsb')
        scan = self.ui.findChild(QPushButton, 'scanDevice')
        scan.clicked.connect(self.scanUsb)
        iso = self.ui.findChild(QPushButton, 'addIso')
        iso.clicked.connect(self.addIsoUi)

        self.loop = QTimer(self)
        self.loop.setInterval(500)
        self.loop.timeout.connect(self.updateUsb)
        self.loop.start()

    def getAvailableFilesystems(self, cbox):
        for f in fs.fileSystems:
            cbox.insertItem(0, str(f), f)

    def getAvailableUSBDevices(self, dev):
        txt = dev.currentText()
        before = len(self.usb_lst)
        usb_lst = fs.getUSBDevices(self.usb_lst)
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
        if before != len(usb_lst):
            self.scanUsb()

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.usb_lst = []
        self.LoadUi()


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MenuCreator()
    d = w.exec_()
    sys.exit(d)
