# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 08:27:20 2019

@author: swati
"""
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QToolTip, QMessageBox
from PyQt5.QtCore import QCoreApplication

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Push Button"
        self.left = 100
        self.top = 100
        self.width = 680
        self.height = 540
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        button = QPushButton("Close", self)
        button.move(200,200)
        button.setToolTip("<h3>This Is Click Button</h3>")
        button.clicked.connect(self.CloseApp)



        self.InitUI()


    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top,self.width, self.height)
        self.show()

    def CloseApp(self):
        reply = QMessageBox.question(self, "Close Message", "Are You Sure To Close Window",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()







App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())