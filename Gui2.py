#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 17:16:20 2019

@author: purnima
"""

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget, QAction, QMessageBox, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QTextEdit
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.widget=Grid(parent=self)
        self.setCentralWidget(self.widget)
        #self.widget.move(0,0)
        
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        helpMenu = mainMenu.addMenu("Help")
        
        openButton = QAction(QIcon("Images/open.png"), 'Open', self)
        openButton.setShortcut("Ctrl+O")
        openButton.setStatusTip("Open MRI (.nii, .nii.gz, .mha)")
        #openButton.triggered.connect(self.OpenMRI)
        fileMenu.addAction(openButton)
        
        openLastButton = QAction(QIcon("Images/open.png"), 'Open last closed', self)
        openLastButton.setShortcut("Ctrl+Shift+T")
        openLastButton.setStatusTip("Open last closed MRI (.nii, .nii.gz, .mha)")
        #openLastButton.triggered.connect(self.OpenLastMRI)
        fileMenu.addAction(openLastButton)
        
        openRecentButton = QAction(QIcon("Images/open.png"), 'Open recent', self)
        openRecentButton.setStatusTip("Open recently closed MRI (.nii, .nii.gz, .mha)")
        #openRecentButton.triggered.connect(self.OpenRecentMRI)
        fileMenu.addAction(openRecentButton)
        
        saveSegButton = QAction(QIcon("Images/saveSegmentedMRI.png"), 'Save segmented MRI', self)
        saveSegButton.setShortcut('Ctrl+S')
        saveSegButton.setStatusTip('Save segmented MRIs')
        #saveSegButton.triggered.connect(self.SaveSegmentedMRI)
        fileMenu.addAction(saveSegButton)
        
        saveMaskButton = QAction(QIcon("Images/saveMask.png"), 'Save mask', self)
        saveMaskButton.setShortcut('Ctrl+Shift+M')
        saveMaskButton.setStatusTip('Save Mask of segmented MRIs')
        #saveMaskButton.triggered.connect(self.SaveMask)
        fileMenu.addAction(saveMaskButton)

        exitButton = QAction(QIcon("Images/close.png"), 'Exit',self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit Application")
        exitButton.triggered.connect(self.CloseApp)
        fileMenu.addAction(exitButton)
        
        aboutButton = QAction(QIcon("Images/about.png"), 'About',self)
        aboutButton.setShortcut("Ctrl+A")
        aboutButton.setStatusTip("About software")
        #aboutButton.triggered.connect(self.AboutSoftware)
        helpMenu.addAction(aboutButton)
        
        tutorialButton = QAction(QIcon("Images/tutorial.png"), 'Tutorial',self)
        tutorialButton.setStatusTip("Demo Tutorial")
        #tutorialButton.triggered.connect(self.AboutSoftware)
        helpMenu.addAction(tutorialButton)
        
        self.widget.but.button.clicked.connect(self.CloseApp)
        
        self.setGeometry(300,300,600,400)
        self.setWindowTitle("FinalGui")
        self.show()
        
    def CloseApp(self):
        reply = QMessageBox.question(self, "Close Message", "Are You Sure To Close Window",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
            
class Grid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        grid_layout=QGridLayout(self)
        
        #self.button.clicked.connect(self.close)
        self.but=buttons(parent=self)
        
        self.text_box = QTextEdit(self)
        
        grid_layout.addWidget(self.text_box, 1, 1, 6, 4)
        grid_layout.addWidget(self.but.button1, 1, 0)
        grid_layout.addWidget(self.but.button2, 2, 0)
        grid_layout.addWidget(self.but.button3, 3, 0)
        grid_layout.addWidget(self.but.button4, 4, 0)
        grid_layout.addWidget(self.but.button5, 5, 0)
        grid_layout.addWidget(self.but.button, 6, 0)
        
class buttons(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.button1=QPushButton("T1")
        self.button1.setEnabled(0)
        #self.button1.resize(200,50)
        
        self.button2=QPushButton("T2")
        self.button2.setEnabled(0)
        
        self.button3=QPushButton("TIC")
        self.button3.setEnabled(0)
        
        self.button4=QPushButton("F")
        self.button4.setEnabled(0)
        
        self.button5=QPushButton("Segment")
        self.button5.setEnabled(0)
        
        self.button=QPushButton("Close")
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())