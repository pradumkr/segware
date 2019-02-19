# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 11:33:02 2019

@author: swati
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *  #ref for icons :https://joekuan.wordpress.com/2015/09/23/list-of-qt-icons/
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from pyqtgraph.Qt import QtCore



class PopUpDLG(QtGui.QDialog):
    def __init__(self, style):
        super(PopUpDLG, self).__init__()
        self.setObjectName("self")
        self.title = "Segware Load Files"
        self.top = 300
        self.left = 300
        self.width = 300
        self.height = 400
        self.setWindowIcon(QtGui.QIcon("images/saveSegmentedMRI.jpg"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.files = {
                'T1': None,
                'T2': None,
                'T1c': None,
                'F': None,
                }
        
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        
        fa5_icon = self.style().standardIcon(getattr(QStyle, 'SP_FileDialogNewFolder'))
        self.T1 = QPushButton(fa5_icon, "select T1",self)
        self.T1.clicked.connect(self.get_t1)
        self.t1_Label = QLabel(self.files['T1'])
        
        self.T2 = QPushButton(fa5_icon, "select T2",self)
        self.T2.clicked.connect(self.get_t2)
        self.t2_Label = QLabel(self.files['T2'])
        
        self.gridLayout.addWidget(self.T1, 0,0,1,2)
        self.gridLayout.addWidget(self.t1_Label,1,0,1,2)
        
        self.gridLayout.addWidget(self.T2, 2,0,1,2)
        self.gridLayout.addWidget(self.t2_Label,3,0,1,2)
        
        if style == 4:
            self.T1c = QPushButton(fa5_icon, "select T1c",self)
            self.T1c.clicked.connect(self.get_t1c)
            self.t1c_Label = QLabel(self.files['T1c'])
            
            self.F = QPushButton(fa5_icon, "select Flair",self)
            self.F.clicked.connect(self.get_f)
            self.f_Label = QLabel(self.files['F'])
            
            self.gridLayout.addWidget(self.T1c, 4,0,1,2)
            self.gridLayout.addWidget(self.t1c_Label,5,0,1,2)
            
            self.gridLayout.addWidget(self.F, 6,0,1,2)
            self.gridLayout.addWidget(self.f_Label,7,0,1,2)
        
        self.add_link = QtGui.QPushButton("Open",self)
        self.gridLayout.addWidget(self.add_link, 8, 0, 1, 1)
        
        self.cancel_link = QtGui.QPushButton("Cancel",self)
        self.gridLayout.addWidget(self.cancel_link,8, 1, 1, 1)
#        self.retranslateUi(self)
        self.cancel_link.clicked.connect(self.reject)
        self.add_link.clicked.connect(self.get_link)
        self.retrunVal = None

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Add link"))
        self.add_link.setText(_translate("Dialog", "Add"))
        self.cancel_link.setText(_translate("Dialog", "Cancel"))

    def get_t1(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;NIfTI -1 (*.nii;*.nii.gz;*.mha)")
        if fileName:
            print(fileName)
            self.files['T1']= fileName
            self.t1_Label.setText(fileName)
            
    def get_t2(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;NIfTI -1 (*.nii;*.nii.gz;*.mha)")
        if fileName:
            print(fileName)
            self.files['T2']= fileName
            self.t2_Label.setText(fileName)
            
    def get_t1c(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;NIfTI -1 (*.nii;*.nii.gz;*.mha)")
        if fileName:
            print(fileName)
            self.files['T1c']= fileName
            self.t1c_Label.setText(fileName)
            
    def get_f(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;NIfTI -1 (*.nii;*.nii.gz;*.mha)")
        if fileName:
            print(fileName)
            self.files['F']= fileName
            self.f_Label.setText(fileName)
            
    def get_link(self):
        self.retrunVal = self.files
        self.accept()

    def exec_(self):
        super(PopUpDLG, self).exec_()
        return self.retrunVal
    
    
class PopUpSegment(QtGui.QDialog):
    def __init__(self):
        super(PopUpSegment, self).__init__()
        self.setObjectName("self")
        self.title = "Segware Segment"
        self.top = 300
        self.left = 300
        self.width = 300
        self.height = 400
        self.setWindowIcon(QtGui.QIcon("images/saveSegmentedMRI.jpg"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.choice = None
        
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        
        segmentLabel = QLabel("Segment:")
        self.gridLayout.addWidget(segmentLabel, 0,0,1,1)
        
        comboBox = QtGui.QComboBox(self)
        comboBox.addItem("--Select--")
        comboBox.addItem("Tumor")
        comboBox.addItem("Cerebrospinal Fluid (CSF)")
        comboBox.addItem("Gray Matter (GM)")
        comboBox.addItem("White Matter (WM)")
        comboBox.activated[str].connect(self.segmentChoice)
        self.gridLayout.addWidget(comboBox, 0,1,1,1)
        
        
        self.add_link = QtGui.QPushButton("Next",self)
        self.gridLayout.addWidget(self.add_link, 1, 0, 1, 1)
        
        self.cancel_link = QtGui.QPushButton("Cancel",self)
        self.gridLayout.addWidget(self.cancel_link,1, 2, 1, 1)
        self.cancel_link.clicked.connect(self.reject)
        self.add_link.clicked.connect(self.get_link)
        self.retrunVal = None
        
    def segmentChoice(self, choice):
            self.choice = choice
            
    def get_link(self):
        self.retrunVal = self.choice
        self.accept()

    def exec_(self):
        super(PopUpSegment, self).exec_()
        return self.retrunVal