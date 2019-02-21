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
    QFileDialog, QGridLayout, QPushButton, QMenu, QGroupBox, QVBoxLayout, QHBoxLayout, QScrollArea, QMessageBox)
import sys
import qtawesome as qta
from pyqtgraph.Qt import QtCore
from openPopup import *
from imagePlot import imagePlot
from utilitiesBackend import *
from medpy.io import load
import numpy as np
from time import sleep

        
        
class Window(QMainWindow):
    EXIT_CODE_REBOOT = -123456789
    def __init__(self):
        super().__init__()
        self.recentFileActs = []
        self.MaxRecentFiles = 5
        self.title = "SegWare"
        self.top = 200
        self.left = 200
        self.width = 1000
        self.height = 500
        self.curData = {
                'T1': None,
                'T2': None,
                'T1c': None,
                'F': None,
                'mask': None,
#                'seg_output': {'csf': None, 'gm': None, 'wm': None, 'tumor': None}
                }
        self.dataAvail = {
                'T1': None,
                'T2': None,
                'T1c': None,
                'F': None,
                'mask': None,
                }
        self.setWindowIcon(QtGui.QIcon("images/saveSegmentedMRI.jpg"))
        
        self.widget = Layout(parent=self)
        self.setCentralWidget(self.widget)
        
        
        self.createActions()
        self.createTools()
        self.createMenus()
        self.statusBar()
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.showMaximized()
        self.files = None
        
        
#        --------------------- 
        
        

    def createActions(self):
        self.viewAct = QAction(QIcon("Images/open.png"), 'View', self, shortcut="Ctrl+O", statusTip="Open MRI (.nii, .nii.gz, .mha)", triggered=self.OpenMRI)
        self.openLastAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogEnd')), 'Open last closed', self, shortcut="Ctrl+Shift+T", statusTip="Open last closed MRI (.nii, .nii.gz, .mha)", triggered=self.OpenLastMRI)
        for i in range(self.MaxRecentFiles):
            self.recentFileActs.append(
                    QAction(self, visible=False,
                            triggered=self.OpenRecentMRI))
        self.segmentAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_DialogSaveButton')), 'Segment Tumor, CSF, GM or WM', self, shortcut="Ctrl+Shift+F", statusTip="Segment", triggered=self.SegementDialog)
        self.saveSegAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_DialogSaveButton')), 'Save segmented MRI', self, shortcut="Ctrl+S", statusTip="Save segmented MRIs", triggered=self.SaveSegmentedMRI)
        self.saveMaskAct = QAction(QIcon("Images/saveMask.png"), 'Save mask', self, shortcut="Ctrl+Shift+M", statusTip="Save Mask of segmented MRIs", triggered=self.SaveMask)
        self.resetAct = QAction(QIcon("Images/about.png"), 'Reset', self, shortcut="Ctrl+C", statusTip="Clear all data", triggered=self.restart)
        self.exitAct = QAction(QIcon("Images/close2.png"), 'Exit', self, shortcut="Ctrl+Q", statusTip="Exit Application", triggered=self.CloseApp)
        self.aboutAct = QAction(QIcon("Images/about.png"), 'About', self, shortcut="Ctrl+A", statusTip="About software", triggered=self.AboutSoftware)
        self.tutorialAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_MessageBoxQuestion')), 'Tutorial', self, statusTip="Demo Tutorial", triggered=self.AboutSoftware)

    def createTools(self):
        self.openTool = self.addToolBar('View')
        self.openTool.addAction(self.viewAct)
        self.openTool.addSeparator()
        self.openTool.addAction(self.segmentAct)
        self.openTool.setMovable(True)
        
    def createMenus(self):
        
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu("File")     
        self.fileMenu.addAction(self.viewAct)
        self.fileMenu.addAction(self.openLastAct)
        
        self.openRecentMenu = QMenu('Open Recent', self)
        self.separatorAct = self.openRecentMenu.addSeparator()
        for i in range(self.MaxRecentFiles):
            self.openRecentMenu.addAction(self.recentFileActs[i])
        self.fileMenu.addMenu(self.openRecentMenu)
        self.fileMenu.addSeparator()
        self.updateRecentFileActions()

        self.fileMenu.addAction(self.segmentAct)
        self.fileMenu.addAction(self.saveSegAct)
        self.fileMenu.addAction(self.saveMaskAct)

        self.fileMenu.addAction(self.resetAct)
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
            
    def SegementDialog(self):
        dialog = PopUpSegment()
        value = dialog.exec_()
        print(value)
        if value:
            self.widget.segmentChoice(value)
        
    def OpenMRI(self):
        print("In open")
        dialog = PopUpDLG(style=4)
        value = dialog.exec_()
        if value:
            print(value)
            self.files = value
            if self.files['T1']:
                self.curData['T1'], _ = load(self.files['T1'])
                self.dataAvail['T1'] = 1
            else:
                self.dataAvail['T1'] = None
            if self.files['T2']:
                self.curData['T2'], _ = load(self.files['T2'])
                self.dataAvail['T2'] = 1
            else:
                self.dataAvail['T2'] = None
            if self.files['T1c']:
                self.curData['T1c'], _ = load(self.files['T1c'])
                self.dataAvail['T1c'] = 1
            else:
                self.dataAvail['T1c'] = None
            if self.files['F']:
                self.curData['F'], _ = load(self.files['F'])
                self.dataAvail['F'] = 1
            else:
                self.dataAvail['F'] = None
            self.widget.createMRIView(self.curData['T1'])
            self.widget.t1Btn.setChecked(True)
            self.widget.dTransverse.setChecked(True)
            self.loadFile(self.files['T1'])
            self.widget.curData = self.curData
            print(self.widget.curData.keys())
            if self.widget.maskView:
                self.widget.maskView.hide()
                self.widget.segmentedView.hide()
            
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
        
    def restart(self):
        qApp.exit(Window.EXIT_CODE_REBOOT)
        

    
        
class Layout(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout()
        self.mriViewPlot = None;
        self.maskViewPlot = None;
        self.segmentedViewPlot = None;
        self.controlLayout = self.createControlLayout()
        self.no_preview = QLabel("No preview Available")
        self.no_preview.setAlignment(Qt.AlignCenter)
        self.mriView = None
        self.maskView = None
        self.segmentedView = None
        self.bfModel = None
        self.grid.addWidget(self.controlLayout, 0, 0)
        if self.mriView:
            self.grid.addWidget(self.mriView, 0, 1)
        else:
            self.grid.addWidget(self.no_preview, 0, 1)
        self.files = None
        self.recentFileActs = []
    
        self.setLayout(self.grid)
        self.curData = {
                'T1': None,
                'T2': None,
                'T1c': None,
                'F': None,
                'mask': None,
#                'seg_output': {'csf': None, 'gm': None, 'wm': None, 'tumor': None}
                }
#    def segment(self):
#        self.createMaskView(self.files['T1'])
#        self.createSegmentedView(self.files['T1'])
#        self.grid.addWidget(self.maskView, 1, 0)
#        self.grid.addWidget(self.segmentedView, 1, 1)
        
    def t1View(self):
        if w.dataAvail['T1']:
            self.mriViewPlot.imv.setImage(self.curData['T1'], xvals=np.linspace(1,self.curData['T1'].shape[0] , self.curData['T1'].shape[0], dtype = 'int32'))
            if self.maskViewPlot:
                data = np.multiply(self.curData['T1'], self.curData['mask'])
                self.maskViewPlot.imv.setImage(self.curData['mask'], xvals=np.linspace(1, self.curData['mask'].shape[0] , self.curData['mask'].shape[0], dtype = 'int32'))
                self.segmentedViewPlot.imv.setImage(data, xvals=np.linspace(1, data.shape[0] , data.shape[0], dtype = 'int32'))
            self.setDimensionalityAndSlice()
            self.slider_value_changed(Window)
        else :
            self.warnMssg("T1")
            
    def t2View(self):
        if w.dataAvail['T2']:
            self.mriViewPlot.imv.setImage(self.curData['T2'], xvals=np.linspace(1,self.curData['T2'].shape[0] , self.curData['T2'].shape[0], dtype = 'int32'))
            if self.maskViewPlot:
                data = np.multiply(self.curData['T2'], self.curData['mask'])
                self.maskViewPlot.imv.setImage(self.curData['mask'], xvals=np.linspace(1, self.curData['mask'].shape[0] , self.curData['mask'].shape[0], dtype = 'int32'))
                self.segmentedViewPlot.imv.setImage(data, xvals=np.linspace(1, data.shape[0] , data.shape[0], dtype = 'int32'))
            self.setDimensionalityAndSlice()
            self.slider_value_changed()
        else:
            self.warnMssg("T2")
    
    def t1cView(self):
        if w.dataAvail['T1c']:
            self.mriViewPlot.imv.setImage(self.curData['T1c'], xvals=np.linspace(1,self.curData['T1c'].shape[0] , self.curData['T1c'].shape[0], dtype = 'int32'))
            if self.maskViewPlot:
                data = np.multiply(self.curData['T1c'], self.curData['mask'])
                self.maskViewPlot.imv.setImage(self.curData['mask'], xvals=np.linspace(1, self.curData['mask'].shape[0] , self.curData['mask'].shape[0], dtype = 'int32'))
                self.segmentedViewPlot.imv.setImage(data, xvals=np.linspace(1, data.shape[0] , data.shape[0], dtype = 'int32'))
            self.setDimensionalityAndSlice()
            self.slider_value_changed()
        else:
            self.warnMssg("T1c")

    def fView(self):
        if w.dataAvail['F']:
            self.mriViewPlot.imv.setImage(self.curData['F'], xvals=np.linspace(1,self.curData['F'].shape[0] , self.curData['F'].shape[0], dtype = 'int32'))
            if self.maskViewPlot:
                data = np.multiply(self.curData['F'], self.curData['mask'])
                self.maskViewPlot.imv.setImage(self.curData['mask'], xvals=np.linspace(1, self.curData['mask'].shape[0] , self.curData['mask'].shape[0], dtype = 'int32'))
                self.segmentedViewPlot.imv.setImage(data, xvals=np.linspace(1, data.shape[0] , data.shape[0], dtype = 'int32'))
            self.setDimensionalityAndSlice()
            self.slider_value_changed()
        else:
            self.warnMssg("Flair")
    
    def warnMssg(self,fileType):
        warn = QMessageBox()
        warn.setIcon(QMessageBox.Information)
        warn.setText(str(fileType)+"File is not loaded please provide"+str(fileType)+" image")
        warn.setWindowTitle("Attention!!!")
        warn.setStandardButtons(QMessageBox.Ok)
        rat = warn.exec_()
        
    def setDimensionalityAndSlice(self):
        self.dTransverse.setChecked(True)
        self.slider_value_changed()
        
    def createControlLayout(self):
        groupBox = QGroupBox("Controls")
        vBoxLayout = QVBoxLayout()
        hboxModality = QHBoxLayout()
        
        modalityLabel = QLabel("Choose Modality:")
        hboxModality.addWidget(modalityLabel)
        self.modalGroup = QButtonGroup()
        
        self.t1Btn = QRadioButton("T1",self)
        self.t1Btn.clicked.connect(self.t1View)
        hboxModality.addWidget(self.t1Btn)

        self.t2Btn = QRadioButton("T2",self)
        self.t2Btn.clicked.connect(self.t2View)
        hboxModality.addWidget(self.t2Btn)
        
        self.t1cBtn = QRadioButton("T1c",self)
        self.t1cBtn.clicked.connect(self.t1cView)
        hboxModality.addWidget(self.t1cBtn)

        self.flairBtn = QRadioButton("FLAIR",self)
        self.flairBtn.clicked.connect(self.fView)
        hboxModality.addWidget(self.flairBtn)
        
        self.modalGroup.addButton(self.t1Btn)
        self.modalGroup.addButton(self.t2Btn)
        self.modalGroup.addButton(self.t1cBtn)
        self.modalGroup.addButton(self.flairBtn)
        
        vBoxLayout.addLayout(hboxModality)

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
        
        self.dimGroup = QButtonGroup()
        dimLabel = QLabel("Choose Dimensionality:")
        slider_layout.addWidget(dimLabel, 2,0,1,2)
        self.dTransverse = QRadioButton("Transverse",self)
        self.dTransverse.clicked.connect(self.transverse_view)
        self.dSaggital = QRadioButton("Saggital",self)
        self.dSaggital.clicked.connect(self.saggital_view)
        self.dCoronal = QRadioButton("Coronal",self)
        self.dCoronal.clicked.connect(self.coronal_view)
        self.dimGroup.addButton(self.dTransverse)
        self.dimGroup.addButton(self.dSaggital)
        self.dimGroup.addButton(self.dCoronal)
        
        slider_layout.addWidget(self.dTransverse, 2,2,1,2)
        slider_layout.addWidget(self.dSaggital, 2,4,1,2)
        slider_layout.addWidget(self.dCoronal, 2,6,1,2)
        vBoxLayout.addLayout(slider_layout)

        groupBox.setLayout(vBoxLayout)
        groupBox.setMinimumSize(300,300)

        return groupBox
    
     
    def transverse_view(self):
        slices = self.mriViewPlot.set_transverse()
        print(slices)
        self.slice_box.setRange(0,slices)
        self.slider.setRange(0, slices)
        if self.maskViewPlot:
            self.maskViewPlot.set_transverse()
            self.segmentedViewPlot.set_transverse()
        self.slider_value_changed()
        
    def saggital_view(self):
        slices = self.mriViewPlot.set_saggital()
        print(slices)
        self.slider.setRange(0, slices)
        self.slice_box.setRange(0,slices)
        if self.maskViewPlot:
            self.maskViewPlot.set_saggital()
            self.segmentedViewPlot.set_saggital()
        self.slider_value_changed()
    
    def coronal_view(self):
        slices = self.mriViewPlot.set_coronal()
        print(slices)
        self.slider.setRange(0, slices)
        self.slice_box.setRange(0,slices)
        if self.maskViewPlot:
            self.maskViewPlot.set_coronal()
            self.segmentedViewPlot.set_coronal()
        self.slider_value_changed()
       
    def slider_value_changed(self):
#        print(str(self.slider.value()))
        self.slice_box.setValue(self.slider.value())
#        self.curLabel.setText("Current Slice: " +str(self.slider.value()))
        self.mriViewPlot.setIndex(self.slider.value())
        if self.maskViewPlot:
            self.maskViewPlot.setIndex(self.slider.value())
            self.segmentedViewPlot.setIndex(self.slider.value())
        
    def slice_box_value_changed(self):
#        print(str(self.slice_box.value()))
        self.slider.setValue(self.slice_box.value())
#        self.curLabel.setText("Current Slice: " +str(self.slider.value()))
        self.mriViewPlot.setIndex(self.slider.value())
        if self.maskViewPlot:
            self.maskViewPlot.setIndex(self.slider.value())
            self.segmentedViewPlot.setIndex(self.slider.value())
    
    def createMRIView(self, data):
        groupBox = QGroupBox("MRI View")
#        print(data.shape)
        self.mriViewPlot = imagePlot(data = data)
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(self.mriViewPlot.imv)
        saveBtn = QPushButton("Save",self)
        vBoxLayout.addWidget(saveBtn)
#        vBoxLayout.addStretch(1)
        groupBox.setLayout(vBoxLayout)
        self.mriView = groupBox
        self.grid.addWidget(self.mriView, 0, 1)
        self.slider.setMaximum(data.shape[0])
        self.slider.setValue(int(data.shape[0]/2))
        self.slice_box.setRange(0,data.shape[0])
        
    
    def createMaskView(self, data):
        groupBox = QGroupBox("Mask View")
        self.maskViewPlot = imagePlot(data)
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(self.maskViewPlot.imv)
        saveBtn = QPushButton("Save",self)
        vBoxLayout.addWidget(saveBtn)
#        vBoxLayout.addStretch(1)
        groupBox.setLayout(vBoxLayout)
        self.maskView = groupBox
        self.grid.addWidget(self.maskView, 1, 0)
    
    def createSegmentedView(self, data):
        groupBox = QGroupBox("Segmentation View")
        self.segmentedViewPlot = imagePlot(data = data)
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(self.segmentedViewPlot.imv)
        saveBtn = QPushButton("Save",self)
        vBoxLayout.addWidget(saveBtn)
#        vBoxLayout.addStretch(1)
        groupBox.setLayout(vBoxLayout)
        self.segmentedView = groupBox
        self.grid.addWidget(self.segmentedView, 1, 1)
        
    def segmentChoice(self, text):
        print(text)
        if text == "Tumor":
            dialog = PopUpDLG(style=4)
            self.setMinimumSize(1000,800)
            value = dialog.exec_()
            if value:
                self.files = value
                self.curData['T1'], _ = load(self.files['T1'])
                self.curData['T2'], _ = load(self.files['T2'])
                self.curData['T1c'], _ = load(self.files['T1c'])
                self.curData['F'], _ = load(self.files['F'])
                self.createMRIView(self.curData['T1'])
                self.t1Btn.setChecked(True)
                self.t1cBtn.setVisible(True)
                self.flairBtn.setVisible(True)
                self.curData = self.curData
                self.tumoreModel = Tumor(self.curData['T1'], self.curData['T2'], self.curData['T1c'], self.curData['F'])
                self.tumoreModel.loadModel()
                print("....predicting")
                self.curData['mask'] = self.tumoreModel.predict()[:,:,:,0]
                self.curData['mask'] = np.transpose(self.curData['mask'],(1,2,0))
                print("...predicted")
                data = np.multiply(self.curData['T1'], self.curData['mask'])
                self.createMaskView(self.curData['mask'])
                self.createSegmentedView(data)
                self.setDimensionalityAndSlice()
        elif text == "--Select--":
            return
        else:
            dialog = PopUpDLG(style=2)
            value = dialog.exec_()
            if value:
                self.files = value
                self.curData['T1'], _ = load(self.files['T1'])
                self.curData['T2'], _ = load(self.files['T2'])
                self.createMRIView(self.curData['T1'])
                self.t1Btn.setChecked(True)
                self.t1cBtn.setVisible(False)
                self.flairBtn.setVisible(False)
                self.curData = self.curData
                if text == "Cerebrospinal Fluid (CSF)":
                    self.bfModel = BrainFluids(self.curData['T1'], self.curData['T2'])
                    print("....predicting")
                    self.bfModel.loadModelAndPredictAll()
                    print("...predicted")
                    self.curData['mask'] = self.bfModel.predictCSF()[0]
                    print(self.curData['mask'].shape)
                    self.createMaskView(self.curData['mask'])
                    data = np.multiply(self.curData['T1'], self.curData['mask'])
                    self.createSegmentedView(data)
                    self.setDimensionalityAndSlice()
                elif text == "Gray Matter (GM)":
                    self.bfModel = BrainFluids(self.curData['T1'], self.curData['T2'])
                    print("....predicting")
                    self.bfModel.loadModelAndPredictAll()
                    print("...predicted")
                    self.curData['mask'] = self.bfModel.predictGM()[0]
                    self.createMaskView(self.curData['mask'])
                    data = np.multiply(self.curData['T1'], self.curData['mask'])
                    self.createSegmentedView(data)
                    self.setDimensionalityAndSlice()
                elif text == "White Matter (WM)":
                    self.bfModel = BrainFluids(self.curData['T1'], self.curData['T2'])
                    print("....predicting")
                    self.bfModel.loadModelAndPredictAll()
                    print("...predicted")
                    self.curData['mask'] = self.bfModel.predictWM()[0]
                    self.createMaskView(self.curData['mask'])
                    data = np.multiply(self.curData['T1'], self.curData['mask'])
                    self.createSegmentedView(data)
                    self.setDimensionalityAndSlice()
#        self.createSegmentedView(self.files['seg_output'])
#        self.createMaskView(self.files['mask_output'])


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