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

import pyqtgraph as pg
import numpy as np
import qtawesome as qta
from pyqtgraph.Qt import QtCore
from medpy.io import load

class PopUpDLG(QtGui.QDialog):
    def __init__(self):
        super(PopUpDLG, self).__init__()
        self.setObjectName("self")
        self.title = "Segware"
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
#        icon = QtGui.QIcon()
#        icon.addPixmap(QtGui.QPixmap("Icons/Plus-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#        self.setWindowIcon(icon)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        
        fa5_icon = self.style().standardIcon(getattr(QStyle, 'SP_FileDialogNewFolder'))
        self.T1 = QPushButton(fa5_icon, "select T1",self)
        self.T1.clicked.connect(self.get_t1)
        self.t1_Label = QLabel(self.files['T1'])
        
        self.T2 = QPushButton(fa5_icon, "select T2",self)
        self.T2.clicked.connect(self.get_t2)
        self.t2_Label = QLabel(self.files['T2'])
        
        self.T1c = QPushButton(fa5_icon, "select T1c",self)
        self.T1c.clicked.connect(self.get_t1c)
        self.t1c_Label = QLabel(self.files['T1c'])
        
        self.F = QPushButton(fa5_icon, "select Flair",self)
        self.F.clicked.connect(self.get_f)
        self.f_Label = QLabel(self.files['F'])
        
        self.gridLayout.addWidget(self.T1, 0,0,1,2)
        self.gridLayout.addWidget(self.t1_Label,1,0,1,2)
        
        self.gridLayout.addWidget(self.T2, 2,0,1,2)
        self.gridLayout.addWidget(self.t2_Label,3,0,1,2)
        
        self.gridLayout.addWidget(self.T1c, 4,0,1,2)
        self.gridLayout.addWidget(self.t1c_Label,5,0,1,2)
        
        self.gridLayout.addWidget(self.F, 6,0,1,2)
        self.gridLayout.addWidget(self.f_Label,7,0,1,2)
        
        self.add_link = QtGui.QPushButton("Save",self)
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
        
        
class Window(QMainWindow):
    MaxRecentFiles = 5
    def __init__(self):
        super().__init__()
        
        self.recentFileActs = []
        self.title = "Segware"
        self.top = 200
        self.left = 200
        self.width = 800
        self.height = 400
        self.setWindowIcon(QtGui.QIcon("images/saveSegmentedMRI.jpg"))
        self.widget = Layout(parent=self)
        self.setCentralWidget(self.widget)
        
        self.createActions()
        self.createMenus()
        self.statusBar()
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()
        self.files = None

    def createActions(self):
        self.openAct = QAction(QIcon("Images/open.png"), 'Open', self, shortcut="Ctrl+O", statusTip="Open MRI (.nii, .nii.gz, .mha)", triggered=self.OpenMRI)
        self.openLastAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogEnd')), 'Open last closed', self, shortcut="Ctrl+Shift+T", statusTip="Open last closed MRI (.nii, .nii.gz, .mha)", triggered=self.OpenLastMRI)
        for i in range(Window.MaxRecentFiles):
            self.recentFileActs.append(
                    QAction(self, visible=False,
                            triggered=self.OpenRecentMRI))
        self.saveSegAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_DialogSaveButton')), 'Save segmented MRI', self, shortcut="Ctrl+S", statusTip="Save segmented MRIs", triggered=self.SaveSegmentedMRI)
        self.saveMaskAct = QAction(QIcon("Images/saveMask.png"), 'Save mask', self, shortcut="Ctrl+Shift+M", statusTip="Save Mask of segmented MRIs", triggered=self.SaveMask)
        self.exitAct = QAction(QIcon("Images/close2.png"), 'Exit', self, shortcut="Ctrl+Q", statusTip="Exit Application", triggered=self.CloseApp)
        self.aboutAct = QAction(QIcon("Images/about.png"), 'About', self, shortcut="Ctrl+A", statusTip="About software", triggered=self.AboutSoftware)
#        flag = qta.icon('fa5.flag')
        self.tutorialAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_MessageBoxQuestion')), 'Tutorial', self, statusTip="Demo Tutorial", triggered=self.AboutSoftware)

        
    def createMenus(self):
        
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu("File")     
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.openLastAct)
        
        self.openRecentMenu = QMenu('Open Recent', self)
        self.separatorAct = self.openRecentMenu.addSeparator()
        for i in range(Window.MaxRecentFiles):
            self.openRecentMenu.addAction(self.recentFileActs[i])
        self.fileMenu.addMenu(self.openRecentMenu)
        self.fileMenu.addSeparator()
        self.updateRecentFileActions()

        
        self.fileMenu.addAction(self.saveSegAct)
        self.fileMenu.addAction(self.saveMaskAct)
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
            
    def OpenMRI(self):
        print("In open")
        dialog = PopUpDLG()
        value = dialog.exec_()
        if value:
            print(value)
            self.files = value
            self.widget.createMRIView(self.files['T1'])
        
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
        del files[Window.MaxRecentFiles:]

        settings.setValue('recentFileList', files)

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, Window):
                widget.updateRecentFileActions()

    def updateRecentFileActions(self):
        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])

        numRecentFiles = min(len(files), Window.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, Window.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()
    
        
class Layout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout()
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
        
#        self.maskView.setHidden(True)
#        self.segmentedView.setHidden(True)
        
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(False)
        scroll.setLayout(self.grid)
        
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(scroll)
        self.setLayout(vLayout)
        
#        self.setLayout(grid)
    def segment(self):
        self.maskView = self.createMaskView()
        self.segmentedView = self.createSegmentedView()
        self.grid.addWidget(self.maskView, 1, 0)
        self.grid.addWidget(self.segmentedView, 1, 1)
        
    def toggleResultView(self):
        self.maskView.setHidden(not self.maskView.isHidden())
        self.segmentedView.setHidden(not self.segmentedView.isHidden())
        
    def createControlLayout(self):
        groupBox = QGroupBox("Controls")
        vBoxLayout = QVBoxLayout()
        hboxModality = QHBoxLayout()
        modalityLabel = QLabel("Choose Modality:")
        hboxModality.addWidget(modalityLabel)
        
        t1Btn = QRadioButton("T1",self)
        hboxModality.addWidget(t1Btn)

        t2Btn = QRadioButton("T2",self)
        hboxModality.addWidget(t2Btn)
        
        t1cBtn = QRadioButton("T1c",self)
        hboxModality.addWidget(t1cBtn)

        flairBtn = QRadioButton("FLAIR",self)
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
        
        self.nameLabel = QLabel("Current Slice : ")
        self.nameLabel.setMaximumHeight(10)
        vBoxLayout.addWidget(self.nameLabel)
        
        self.slice_box = QSpinBox()
        self.slice_box.setRange(0,144)
        self.slice_box.valueChanged.connect(self.slice_box_value_changed)
        slider_layout = QGridLayout()
        slider_layout.addWidget(self.slider, 0,0,1,5);
        slider_layout.addWidget(self.slice_box,0,5,1,1);
        fa5_icon = qta.icon('fa5.paper-plane')
        d1 = QPushButton(fa5_icon, "Transverse",self)
        d1.clicked.connect(self.transverse_view)
        d2 = QPushButton(fa5_icon, "Saggital",self)
        d2.clicked.connect(self.saggital_view)
        d3 = QPushButton(fa5_icon, "Coronal",self)
        d3.clicked.connect(self.coronal_view)
        slider_layout.addWidget(d1, 1,0,1,2)
        slider_layout.addWidget(d2, 1,2,1,2)
        slider_layout.addWidget(d3, 1,4,1,2)
        vBoxLayout.addLayout(slider_layout)

        groupBox.setLayout(vBoxLayout)
        groupBox.setMinimumSize(300,300)

        return groupBox
    
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
        self.nameLabel.setText("Current Slice: " +str(self.slider.value()))
        self.pgcustom1.setIndex(self.slider.value())
        self.pgcustom2.setIndex(self.slider.value())
        self.pgcustom3.setIndex(self.slider.value())
        
    def slice_box_value_changed(self):
#        print(str(self.slice_box.value()))
        self.slider.setValue(self.slice_box.value())
        self.nameLabel.setText("Current Slice: " +str(self.slider.value()))
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
        
    
    def createMaskView(self):
        groupBox = QGroupBox("Mask View")
#        self.pgcustom = imagePlot(fileName = 'DP_preprocessed.nii.gz')
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(self.pgcustom2.imv)
        saveBtn = QPushButton("Save",self)
        vBoxLayout.addWidget(saveBtn)
#        vBoxLayout.addStretch(1)
        groupBox.setLayout(vBoxLayout)
        return groupBox
    
    def createSegmentedView(self):
        groupBox = QGroupBox("Segmentation View")
#        self.pgcustom = imagePlot(fileName = 'DP_preprocessed.nii.gz')
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(self.pgcustom3.imv)
        saveBtn = QPushButton("Save",self)
        vBoxLayout.addWidget(saveBtn)
#        vBoxLayout.addStretch(1)
        groupBox.setLayout(vBoxLayout)

        return groupBox
    
    def style_choice(self, text):
        print(text)
        self.segment()
        self.setMinimumSize(800,800)

        
        
class imagePlot(pg.ImageView):
    
    def __init__(self, fileName):
        if fileName:
            dp_input, image_header = load(fileName)
            self.data = np.asarray(dp_input)
        
            # Interpret image data as row-major instead of col-major
            pg.setConfigOptions(imageAxisOrder='col-major')
            self.imv = pg.ImageView()
    #        self.imv.view.setBackgroundColor('#f0f0f0')
            self.imv.timeLine.setPen('y', width=10)
            self.imv.ui.splitter.setChildrenCollapsible(False)
            self.imv.ui.splitter.setStretchFactor(8,1)
            self.imv.timeLine.setHoverPen('r', width=12)
            self.imv.view.setMenuEnabled(False)  
            roi = self.imv.getRoiPlot()
            slider = roi.plotItem.getViewWidget()
            slider.setMaximumHeight(60)
            roi.plotItem.setMenuEnabled(False)
            ## Display the data and assign each frame a time value from 1.0 to 3.0
            self.imv.setImage(self.data, xvals=np.linspace(1, 144, self.data.shape[0], dtype = 'int32'))
            ## Set a custom color map
            colors = [
                (0, 0, 0),
                (45, 5, 61),
                (84, 42, 55),
                (150, 87, 60),
                (208, 171, 141),
                (255, 255, 255)
            ]
            self.cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
            self.imv.setColorMap(self.cmap)
            self.imv.setCurrentIndex(72)
            self.imv.ui.roiBtn.hide()
            self.imv.ui.menuBtn.hide()
        
    def setIndex(self, index):
        self.imv.setCurrentIndex(index)
        
    def set_transverse(self):
        data = np.transpose(self.data, (0,1,2))
        self.imv.setImage(data, xvals=np.linspace(1, data.shape[0], data.shape[0], dtype = 'int32'))
        self.imv.setCurrentIndex(int(data.shape[0]/2))
        return data.shape[0]
    
    def set_coronal(self):
        data = np.transpose(self.data, (2,1,0))
        self.imv.setImage(data, xvals=np.linspace(1, data.shape[0], data.shape[0], dtype = 'int32'))
        self.imv.setCurrentIndex(int(data.shape[0]/2))
        return data.shape[0]
    
    def set_saggital(self):
        data = np.transpose(self.data, (1,0,2))
        self.imv.setImage(data, xvals=np.linspace(1, data.shape[0], data.shape[0], dtype = 'int32'))
        self.imv.setCurrentIndex(int(data.shape[0]/2))
        return data.shape[0]
#        'xMin', 'xMax', 'yMin', 'yMax', 'minXRange', 'maxXRange', 'minYRange', 'maxYRange'
#        self.setLimits(())

#screen size determine 
App = QtCore.QCoreApplication.instance()
    # creating main window
if App is None:
    App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())