#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 17:16:20 2019

@author: purnima
"""

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QWidget, QAction, QScrollArea, QScrollBar,
                             QMessageBox, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QTextEdit)
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
        openButton.triggered.connect(self.OpenMRI)
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
        
        self.widget.but.button5.clicked.connect(self.enb)
        
        self.setGeometry(300,300,600,400)
        self.setWindowTitle("FinalGui")
        self.show()
        
    def CloseApp(self):
        reply = QMessageBox.question(self, "Close Message", "Are You Sure To Close Window",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
            
    def OpenMRI(self):
        print("In open")
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;NIfTI -1 (*.nii;*.nii.gz;*.mha)")
        if fileName:
            print(fileName)
            
        self.widget.but.button1.setEnabled(True)
        self.widget.but.button2.setEnabled(True)
        self.widget.but.button3.setEnabled(True)
        self.widget.but.button4.setEnabled(True)
        self.widget.but.button5.setEnabled(True)
            
    def enb(self):
        self.widget.but.button5.setEnabled(False)
        
        #self.bar=Scroll(parent=self)
        
        #self.widget.grid_layout.addWidget(self.bar.s3, 6, 5)
        #self.setCentralWidget(self.bar)
            
class Grid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        grid_layout=QGridLayout(self)
        
        #self.button.clicked.connect(self.close)
        self.but=buttons(parent=self)
        
        self.text_box1 = QTextEdit(self)
        self.text_box2 = QTextEdit(self)
        self.text_box3 = QTextEdit(self)
        
        grid_layout.addWidget(self.text_box1, 0, 1, 6, 1)
        grid_layout.addWidget(self.but.button1, 0, 0, 1,1)
        grid_layout.addWidget(self.but.button2, 1, 0,1,1)
        grid_layout.addWidget(self.but.button3, 2, 0,1,1)
        grid_layout.addWidget(self.but.button4, 3, 0,1,1)
        grid_layout.addWidget(self.but.button5, 4, 0,1,1)
        grid_layout.addWidget(self.but.button, 5, 0,1,1)
        grid_layout.addWidget(self.text_box2, 6, 0, 1, 1)
        grid_layout.addWidget(self.text_box3, 6, 1, 1, 1)
        
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
        
class Scroll(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.s3 = QScrollBar()
        self.s3.setMaximum(255)
        #self.s3.sliderMoved.connect(self.sliderval)
        
        
        
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())