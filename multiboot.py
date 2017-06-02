#!/usr/bin/env python
import sys
# for pathwalk
# import os
import menu
import fs

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
# from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi


class IsoDialog(QDialog):

    @pyqtSlot()
    def selectDistribution(self):
        modIdx = self.distList.selectedIndexes()[0]
        print(modIdx, modIdx.row())
        print(self.isos[modIdx.row()])
        self.dist = self.isos[modIdx.row()]
        self.accept()

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.isos = [
            'Gnome Debian 9 x64',
            'XFCE Debian 9 x64',
            'Linux Mint 18.4 Cinnamon x64',
            'Linux Mint Debian Edition (2) x64',
            'Ubuntu 16.04 (latest) Mate x64'
        ]
        self.loadUi()
        self.dist = None

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
        self.distList = view
        add = ui.findChild(QPushButton, 'add')
        add.clicked.connect(self.selectDistribution)


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

    def addDist(self, d):
        m = None
        iso_label = 'linux.iso'
        if 'Debian' in d:
            m = menu.DebianLiveISO(name=d)
            iso_label = m.iso

        twi = QTreeWidgetItem([d, iso_label, ''], 0)
        twi.setData(4, 0, m)
        mtree = self.ui.findChild(QTreeWidget, 'menuTree')
        mtree.addTopLevelItem(twi)

    @pyqtSlot()
    def addIsoUi(self):
        iso = IsoDialog(self)
        a = iso.exec_()
        if a > 0:
            self.addDist(iso.dist)

    @pyqtSlot()
    def scanUsb(self):
        dev = self.dev.currentData()
        if dev is not None:
            parts = dev.partitions()
            if parts[0][0] == '1':
                if 'fat' in parts[0][1]:
                    idx = self.fs.findText('vfat')
                else:
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
