# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 11:00:15 2019

@author: swati
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *  #ref for icons :https://joekuan.wordpress.com/2015/09/23/list-of-qt-icons/
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QSpinBox, QSlider,QApplication, QMainWindow,QWidget, QAction, QMessageBox, QLabel, QRadioButton, 
    QFileDialog, QGridLayout, QPushButton, QMenu, QGroupBox, QVBoxLayout, QHBoxLayout, QScrollArea)
import sys
#import pyqtgraph as pg
#import numpy as np
import qtawesome as qta
from pyqtgraph.Qt import QtCore
#from medpy.io import load
from openPopup import PopUpDLG
from imagePlot import imagePlot
        
        
class Window(QMainWindow):
    MaxRecentFiles = 5
    EXIT_CODE_REBOOT = -123456789
    def __init__(self):
        super().__init__()
        self.recentFileActs = []
        self.title = "SegWare"
        self.top = 200
        self.left = 200
        self.width = 1000
        self.height = 500
        self.setWindowIcon(QtGui.QIcon("images/saveSegmentedMRI.jpg"))
        
        self.widget = Layout(parent=self)
        self.setCentralWidget(self.widget)
        
        
        self.createActions()
        self.createMenus()
        self.statusBar()
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.showMaximized()
        self.files = None
        
        
#        --------------------- 
        
        

    def createActions(self):
        self.openAct = QAction(QIcon("Images/open.png"), 'Open', self, shortcut="Ctrl+O", statusTip="Open MRI (.nii, .nii.gz, .mha)", triggered=self.widget.OpenMRI)
        self.openLastAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogEnd')), 'Open last closed', self, shortcut="Ctrl+Shift+T", statusTip="Open last closed MRI (.nii, .nii.gz, .mha)", triggered=self.widget.OpenLastMRI)
        for i in range(Window.MaxRecentFiles):
            self.widget.recentFileActs.append(
                    QAction(self, visible=False,
                            triggered=self.widget.OpenRecentMRI))
        self.saveSegAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_DialogSaveButton')), 'Save segmented MRI', self, shortcut="Ctrl+S", statusTip="Save segmented MRIs", triggered=self.widget.SaveSegmentedMRI)
        self.saveMaskAct = QAction(QIcon("Images/saveMask.png"), 'Save mask', self, shortcut="Ctrl+Shift+M", statusTip="Save Mask of segmented MRIs", triggered=self.widget.SaveMask)
<<<<<<< HEAD
<<<<<<< HEAD
#        self.resetAct = QAction(QIcon("Images/about.png"), 'Reset', self, shortcut="Ctrl+C", statusTip="Clear all data", triggered=self.toggleResultView)
        self.exitAct = QAction(QIcon("Images/close2.png"), 'Exit', self, shortcut="Ctrl+Q", statusTip="Exit Application", triggered=self.CloseApp)
        self.aboutAct = QAction(QIcon("Images/about.png"), 'About', self, shortcut="Ctrl+A", statusTip="About software", triggered=self.widget.AboutSoftware)
=======
=======
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
        self.resetAct = QAction(QIcon("Images/about.png"), 'Reset', self, shortcut="Ctrl+C", statusTip="Clear all data", triggered=self.toggleResultView)
        self.exitAct = QAction(QIcon("Images/close2.png"), 'Exit', self, shortcut="Ctrl+Q", statusTip="Exit Application", triggered=self.CloseApp)
        self.aboutAct = QAction(QIcon("Images/about.png"), 'About', self, shortcut="Ctrl+A", statusTip="About software", triggered=self.widget.AboutSoftware)
#        flag = qta.icon('fa5.flag')
<<<<<<< HEAD
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
=======
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
        self.tutorialAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_MessageBoxQuestion')), 'Tutorial', self, statusTip="Demo Tutorial", triggered=self.widget.AboutSoftware)

        
    def createMenus(self):
        
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu("File")     
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.openLastAct)
        
        self.openRecentMenu = QMenu('Open Recent', self)
        self.separatorAct = self.openRecentMenu.addSeparator()
        for i in range(Window.MaxRecentFiles):
            self.openRecentMenu.addAction(self.widget.recentFileActs[i])
        self.fileMenu.addMenu(self.openRecentMenu)
        self.fileMenu.addSeparator()
        self.widget.updateRecentFileActions()

        
        self.fileMenu.addAction(self.saveSegAct)
        self.fileMenu.addAction(self.saveMaskAct)
<<<<<<< HEAD
<<<<<<< HEAD
#        self.fileMenu.addAction(self.resetAct)
=======
        self.fileMenu.addAction(self.resetAct)
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
=======
        self.fileMenu.addAction(self.resetAct)
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
        self.fileMenu.addAction(self.exitAct)
        self.menuBar().addSeparator()
        self.helpMenu = self.mainMenu.addMenu("Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.tutorialAct)

    def CloseApp(self):
        reply = QMessageBox.question(self, "Close Message", "Are You Sure To Close Window",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
            
    def toggleResultView(self):
#        self.widget.maskView.setHidden(not self.widget.maskView.isHidden())
#        self.widget.segmentedView.setHidden(not self.widget.segmentedView.isHidden())
#        super().setGeometry(200,200,1000,500)
#        self.grid.removeWidget(self.maskView)
#        self.grid.removeWidget(self.segmentedView)
#        self.maskView.deleteLater()
#        self.setMinimumSize(1000,500)
        
#        self.widget.maskView.hide()
#        self.widget.segmentedView.hide()
#        self.widget.mriView.hide()
#        self.widget.grid.addWidget(self.widget.no_preview, 0, 1)
        self.restart()
#        self.setGeometry(self.top, self.left, self.width, self.height)
#        self.setGeometry()
#        self.resize(1000,500)
        
    def restart(self):
        qApp.exit(Window.EXIT_CODE_REBOOT)
        
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
#    def set_Geometry(self):
#        self.toggleResultView()
#        self.widget.setMinimumSize(700,300)
#        self.widget.controlLayout.resize(400,400)
#        self.widget.mriView.resize(400,400)
        
<<<<<<< HEAD
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
=======
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
    
        
class Layout(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.grid = QGridLayout(self.scrollAreaWidgetContents)
        self.MaxRecentFiles = 5
        self.pgcustom1 = None;
        self.pgcustom2 = imagePlot(fileName = 'DP_preprocessed.nii.gz')
        self.pgcustom3 = imagePlot(fileName = 'DP_preprocessed.nii.gz')
        self.controlLayout = self.createControlLayout()
#        self.mriView = self.createMRIView()
        self.no_preview = QLabel("No preview Available")
        self.no_preview.setAlignment(Qt.AlignCenter)
        self.mriView = None
        self.maskView = None
        self.segmentedView = None
        self.grid.addWidget(self.controlLayout, 0, 0)
        if self.mriView:
            self.grid.addWidget(self.mriView, 0, 1)
        else:
            self.grid.addWidget(self.no_preview, 0, 1)
        
#        scroll = QScrollArea()
#        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
#        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#        scroll.setWidgetResizable(False)
#        scroll.setLayout(self.grid)
        
#        vLayout = QVBoxLayout(self)
#        vLayout.addWidget(scroll)
#        self.setLayout(vLayout)
        self.files = None
        self.recentFileActs = []
    
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)
#        self.setLayout(grid)
<<<<<<< HEAD
<<<<<<< HEAD
        
#    def segment(self):
#        self.createMaskView(self.files['T1'])
#        self.createSegmentedView(self.files['T1'])
#        self.grid.addWidget(self.maskView, 1, 0)
#        self.grid.addWidget(self.segmentedView, 1, 1)
        
    def t1View(self):
        self.createMRIView(self.files['T1'])
        if self.files['seg_output']:
            self.createSegmentedView(self.files['seg_output']['T1'])
        if self.files['mask_output']:
            self.createMaskView(self.files['mask_output'])
            
    def t2View(self):
        self.createMRIView(self.files['T2'])
        if self.files['seg_output']:
            self.createSegmentedView(self.files['seg_output']['T2'])
        if self.files['mask_output']:
            self.createMaskView(self.files['mask_output'])
    
    def t1cView(self):
        self.createMRIView(self.files['T1c'])
        if self.files['seg_output']:
            self.createSegmentedView(self.files['seg_output']['T1c'])
        if self.files['mask_output']:
            self.createMaskView(self.files['mask_output'])
    
    def fView(self):
        self.createMRIView(self.files['F'])
        if self.files['seg_output']:
            self.createSegmentedView(self.files['seg_output']['F'])
        if self.files['mask_output']:
            self.createMaskView(self.files['mask_output'])
        
=======
=======
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
    def segment(self):
        self.createMaskView(self.files['T1'])
        self.createSegmentedView(self.files['T1'])
#        self.grid.addWidget(self.maskView, 1, 0)
#        self.grid.addWidget(self.segmentedView, 1, 1)
        
<<<<<<< HEAD
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
=======
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
    def createControlLayout(self):
        groupBox = QGroupBox("Controls")
        vBoxLayout = QVBoxLayout()
        hboxModality = QHBoxLayout()
        
        modalityLabel = QLabel("Choose Modality:")
        hboxModality.addWidget(modalityLabel)
        
        t1Btn = QRadioButton("T1",self)
<<<<<<< HEAD
<<<<<<< HEAD
        t1Btn.clicked.connect(self.t1View)
        hboxModality.addWidget(t1Btn)

        t2Btn = QRadioButton("T2",self)
        t2Btn.clicked.connect(self.t2View)
        hboxModality.addWidget(t2Btn)
        
        t1cBtn = QRadioButton("T1c",self)
        t1cBtn.clicked.connect(self.t1cView)
        hboxModality.addWidget(t1cBtn)

        flairBtn = QRadioButton("FLAIR",self)
        flairBtn.clicked.connect(self.fView)
=======
=======
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
        hboxModality.addWidget(t1Btn)

        t2Btn = QRadioButton("T2",self)
        hboxModality.addWidget(t2Btn)
        
        t1cBtn = QRadioButton("T1c",self)
        hboxModality.addWidget(t1cBtn)

        flairBtn = QRadioButton("FLAIR",self)
<<<<<<< HEAD
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
=======
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
        hboxModality.addWidget(flairBtn)
        t1Btn.setChecked(True)
        
        vBoxLayout.addLayout(hboxModality)

        hbox = QHBoxLayout()
        segmentLabel = QLabel("Segment:")
        hbox.addWidget(segmentLabel)
        comboBox = QtGui.QComboBox(self)
        comboBox.addItem("-Select-")
        comboBox.addItem("Tumor")
        comboBox.addItem("Cerebrospinal Fluid (CSF)")
        comboBox.addItem("Gray Matter (GM)")
        comboBox.addItem("White Matter (WM)")
        comboBox.activated[str].connect(self.style_choice)
        hbox.addWidget(comboBox)
        vBoxLayout.addLayout(hbox)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setMinimum(0)
        self.slider.setMaximum(144)
        self.slider.setValue(0)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.slider_value_changed)
#        vBoxLayout.addWidget(self.slider)
        
        self.slice_box = QSpinBox()
        self.slice_box.setRange(0,144)
        self.slice_box.valueChanged.connect(self.slice_box_value_changed)
        
        slider_layout = QGridLayout()
        
        self.setSliceLabel = QLabel("Set Slice Number:")
        slider_layout.addWidget(self.setSliceLabel, 0,0)
        
        slider_layout.addWidget(self.slider, 0,2,1,6)
        
        self.curLabel = QLabel("Current Slice : ")
        slider_layout.addWidget(self.curLabel, 1,2,1,3)
        slider_layout.addWidget(self.slice_box,1,5,1,3);
#        slider_layout.addSeparator()
        
        dimLabel = QLabel("Choose Dimensionality:")
        slider_layout.addWidget(dimLabel, 2,0,1,2)
        d1 = QRadioButton("Transverse",self)
        d1.clicked.connect(self.transverse_view)
        d2 = QRadioButton("Saggital",self)
        d2.clicked.connect(self.saggital_view)
        d3 = QRadioButton("Coronal",self)
        d3.clicked.connect(self.coronal_view)
        slider_layout.addWidget(d1, 2,2,1,2)
        slider_layout.addWidget(d2, 2,4,1,2)
        slider_layout.addWidget(d3, 2,6,1,2)
        vBoxLayout.addLayout(slider_layout)

        groupBox.setLayout(vBoxLayout)
        groupBox.setMinimumSize(300,300)

        return groupBox
    
    def OpenMRI(self):
        print("In open")
        dialog = PopUpDLG()
        value = dialog.exec_()
        if value:
            print(value)
            self.files = value
            self.createMRIView(self.files['T1'])
#            self.setMaximumSize(900,450)
#            self.setMinimumSize(900,450)
            if self.maskView:
                self.maskView.hide()
                self.segmentedView.hide()
            
    def OpenLastMRI(self):
        print("In open last MRI")
        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])
        if(files[0]):
            fileName = files[0]
            print(fileName)
            self.loadFile(fileName)
        
    def OpenRecentMRI(self):
        print("In open recent MRI")
        action = self.sender()
        if action:
            fileName = action.data()
            self.loadFile(fileName)

    def SaveSegmentedMRI(self):
        print("In SaveSegmentedMRI") 
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;NIfTI -1 (*.nii;*.nii.gz;*.mha);;NumPy array(*.npy;*.npz);;Images JPEG(*.jpg,*.png,*.jpeg)")
        if fileName:
            print(fileName)
            self.saveFile(fileName)

    def SaveMask(self):
        print("In save mask")
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;NIfTI -1 (*.nii;*.nii.gz;*.mha);;NumPy array(*.npy;*.npz);;Images JPEG(*.jpg,*.png,*.jpeg)")
        if fileName:
            print(fileName)
            self.saveFile(fileName)
        
    def AboutSoftware(self):
        print("In AboutSoftware") 
        QMessageBox.about(self, "About Recent Files",
                "The <b>Recent Files</b> example demonstrates how to provide "
                "a recently used file menu in a Qt application.")
        
    def loadFile(self, fileName):
        print("Loading...", fileName)
        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)
    
    def saveFile(self, fileName):
        print("Saving...", fileName)
        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File saved", 2000)
    
    def setCurrentFile(self, fileName):
        self.curFile = fileName
        if self.curFile:
            self.setWindowTitle("%s - Recent Files" % self.strippedName(self.curFile))
        else:
            self.setWindowTitle("Recent Files")

        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])

        try:
            files.remove(fileName)
        except ValueError:
            pass

        files.insert(0, fileName)
        del files[self.MaxRecentFiles:]

        settings.setValue('recentFileList', files)

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, Window):
                widget.updateRecentFileActions()

    def updateRecentFileActions(self):
        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])

        numRecentFiles = min(len(files), self.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, self.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

#        self.separatorAct.setVisible((numRecentFiles > 0))
        
    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()
    
    def transverse_view(self):
        slices = self.pgcustom1.set_transverse()
        print(slices)
        self.slice_box.setRange(0,slices)
        self.slider.setRange(0, slices)
        self.pgcustom2.set_transverse()
        self.pgcustom3.set_transverse()
        
    def saggital_view(self):
        slices = self.pgcustom1.set_saggital()
        print(slices)
        self.slider.setRange(0, slices)
        self.slice_box.setRange(0,slices)
        self.pgcustom2.set_saggital()
        self.pgcustom3.set_saggital()
    
    def coronal_view(self):
        slices = self.pgcustom1.set_coronal()
        print(slices)
        self.slider.setRange(0, slices)
        self.slice_box.setRange(0,slices)
        self.pgcustom2.set_coronal()
        self.pgcustom3.set_coronal()
       
    def slider_value_changed(self):
#        print(str(self.slider.value()))
        self.slice_box.setValue(self.slider.value())
#        self.curLabel.setText("Current Slice: " +str(self.slider.value()))
        self.pgcustom1.setIndex(self.slider.value())
        self.pgcustom2.setIndex(self.slider.value())
        self.pgcustom3.setIndex(self.slider.value())
        
    def slice_box_value_changed(self):
#        print(str(self.slice_box.value()))
        self.slider.setValue(self.slice_box.value())
#        self.curLabel.setText("Current Slice: " +str(self.slider.value()))
        self.pgcustom1.setIndex(self.slider.value())
        self.pgcustom2.setIndex(self.slider.value())
        self.pgcustom3.setIndex(self.slider.value())
    
    def createMRIView(self, fileName):
        groupBox = QGroupBox("MRI View")
        print(fileName)
        self.pgcustom1 = imagePlot(fileName = fileName)
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(self.pgcustom1.imv)
        saveBtn = QPushButton("Save",self)
        vBoxLayout.addWidget(saveBtn)
#        vBoxLayout.addStretch(1)
        groupBox.setLayout(vBoxLayout)
        self.mriView = groupBox
        self.grid.addWidget(self.mriView, 0, 1)
        
    
    def createMaskView(self,filename):
        groupBox = QGroupBox("Mask View")
        self.pgcustom2 = imagePlot(fileName = filename)
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(self.pgcustom2.imv)
        saveBtn = QPushButton("Save",self)
        vBoxLayout.addWidget(saveBtn)
#        vBoxLayout.addStretch(1)
        groupBox.setLayout(vBoxLayout)
        self.maskView = groupBox
        self.grid.addWidget(self.maskView, 1, 0)
    
    def createSegmentedView(self, filename):
        groupBox = QGroupBox("Segmentation View")
        self.pgcustom3 = imagePlot(fileName = filename)
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(self.pgcustom3.imv)
        saveBtn = QPushButton("Save",self)
        vBoxLayout.addWidget(saveBtn)
#        vBoxLayout.addStretch(1)
        groupBox.setLayout(vBoxLayout)
        self.segmentedView = groupBox
        self.grid.addWidget(self.segmentedView, 1, 1)
        
    def style_choice(self, text):
        print(text)
<<<<<<< HEAD
<<<<<<< HEAD
#        self.segment()
        self.setMinimumSize(1000,800)
        if text == "-Select-":
            return
        elif text == "Cerebrospinal Fluid (CSF)":
            
        elif text == "Gray Matter (GM)":
            
        else:
            
        self.createSegmentedView(self.files['seg_output'])
        self.createMaskView(self.files['mask_output'])
        
=======
        self.segment()
        self.setMinimumSize(1000,800)
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
=======
        self.segment()
        self.setMinimumSize(1000,800)
>>>>>>> 013bb9c734a0d8a8bf4a2cdf3871392f941308ef
        

#        'xMin', 'xMax', 'yMin', 'yMax', 'minXRange', 'maxXRange', 'minYRange', 'maxYRange'
#        self.setLimits(())

#screen size determine 

if __name__ == "__main__":
    c = Window.EXIT_CODE_REBOOT 
    while c == Window.EXIT_CODE_REBOOT:
        App = QtCore.QCoreApplication.instance()
        # creating main window
        if App is None:
            App = QApplication(sys.argv)
        w = Window()
        w.show()
        c = App.exec_()
        App =  None
    #    sys.exit(App.exec())