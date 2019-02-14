# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 11:00:15 2019

@author: swati
"""

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget, QAction, QMessageBox, QFileDialog, QGridLayout, QTextEdit, QPushButton
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "QMenuBar"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self.InitWindow()


    def InitWindow(self):
        
        self.widget = EmailBlast(parent=self)
        self.setCentralWidget(self.widget)
        
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
        openLastButton.triggered.connect(self.OpenLastMRI)
        fileMenu.addAction(openLastButton)
        
        openRecentButton = QAction(QIcon("Images/open.png"), 'Open recent', self)
        openRecentButton.setStatusTip("Open recently closed MRI (.nii, .nii.gz, .mha)")
        openRecentButton.triggered.connect(self.OpenRecentMRI)
        fileMenu.addAction(openRecentButton)
        
        saveSegButton = QAction(QIcon("Images/saveSegmentedMRI.png"), 'Save segmented MRI', self)
        saveSegButton.setShortcut('Ctrl+S')
        saveSegButton.setStatusTip('Save segmented MRIs')
        saveSegButton.triggered.connect(self.SaveSegmentedMRI)
        fileMenu.addAction(saveSegButton)
        
        saveMaskButton = QAction(QIcon("Images/saveMask.png"), 'Save mask', self)
        saveMaskButton.setShortcut('Ctrl+Shift+M')
        saveMaskButton.setStatusTip('Save Mask of segmented MRIs')
        saveMaskButton.triggered.connect(self.SaveMask)
        fileMenu.addAction(saveMaskButton)

        exitButton = QAction(QIcon("Images/close.png"), 'Exit',self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit Application")
        exitButton.triggered.connect(self.CloseApp)
        fileMenu.addAction(exitButton)
        
        aboutButton = QAction(QIcon("Images/about.png"), 'About',self)
        aboutButton.setShortcut("Ctrl+A")
        aboutButton.setStatusTip("About software")
        aboutButton.triggered.connect(self.AboutSoftware)
        helpMenu.addAction(aboutButton)
        
        tutorialButton = QAction(QIcon("Images/tutorial.png"), 'Tutorial',self)
        tutorialButton.setStatusTip("Demo Tutorial")
        tutorialButton.triggered.connect(self.AboutSoftware)
        helpMenu.addAction(tutorialButton)


        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
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
        
    def OpenLastMRI(self):
        print("In open last MRI")
        
        
    def OpenRecentMRI(self):
        print("In open recent MRI")

    def SaveSegmentedMRI(self):
        print("In SaveSegmentedMRI") 
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;NIfTI -1 (*.nii;*.nii.gz;*.mha);;NumPy array(*.npy;*.npz);;Images JPEG(*.jpg,*.png,*.jpeg)")
        if fileName:
            print(fileName)

    def SaveMask(self):
        print("In save mask")
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;NIfTI -1 (*.nii;*.nii.gz;*.mha);;NumPy array(*.npy;*.npz);;Images JPEG(*.jpg,*.png,*.jpeg)")
        if fileName:
            print(fileName)
        
    def AboutSoftware(self):
        print("In AboutSoftware")  
        
class EmailBlast(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # create and set layout to place widgets
        grid_layout = QGridLayout(self)

        self.text_box = QTextEdit(self)
        self.save_button = QPushButton('Save')
        self.clear_button = QPushButton('Clear')
        self.open_button = QPushButton('Open')
        # add widgets to layout. Params are:
        # (widget, fromRow, fromColumn, rowSpan=1, columnSpan=1)
        grid_layout.addWidget(self.text_box, 0, 0, 1, 3)
        grid_layout.addWidget(self.save_button, 1, 0)
        grid_layout.addWidget(self.clear_button, 1, 1)
        grid_layout.addWidget(self.open_button, 1, 2)

        
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())