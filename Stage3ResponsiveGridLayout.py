import sys
from PyQt5 import QtWidgets

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pyqtgraph as pg
import numpy as np

from pyqtgraph.Qt import QtCore
from medpy.io import load


#screen size determine 
app = QtCore.QCoreApplication.instance()
    # creating main window
if app is None:
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()    
screen = app.primaryScreen()
if screen:
    size = screen.size()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window_widget = Grid(parent=self)
        #set minimum window size
        self.setMinimumSize(QSize(600,400))

        self.setGeometry(0,0,size.width(), size.height())#top,left,width,height

        self.setCentralWidget(self.window_widget)
        # filling up a menu bar
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

    def CloseApp(self):
        reply = QMessageBox.question(self, "Close Message", "Are You Sure To Close Window",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            
    def OpenMRI(self):
        print("In open")
        
    def OpenLastMRI(self):
        print("In open last MRI")
        
    def OpenRecentMRI(self):
        print("In open recent MRI")

    def SaveMask(self):
        print("In save mask")
        
    def AboutSoftware(self):
        print("In AboutSoftware")    
        
    def SaveSegmentedMRI(self):
        print("In SaveSegmentedMRI")   

class Grid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        grid_layout= QGridLayout(self)
        
        #self.button.clicked.connect(self.close)
        
        self.pgcustom = imagePlot()
        self.pgcustom2 = imagePlot1()
        self.pgcustom3 = imagePlot2()
        vBoxLayout = QVBoxLayout()

        #add buttons for part 1
        button1=QPushButton("T1",self)
        vBoxLayout.addWidget(button1)

        button2=QPushButton("T2",self)
        vBoxLayout.addWidget(button2)
        
        button3=QPushButton("TC",self)
        vBoxLayout.addWidget(button3)

        button4=QPushButton("F",self)
        vBoxLayout.addWidget(button4)

        button5=QPushButton("SEGMENT",self)
        vBoxLayout.addWidget(button5)
#        button5.clicked.connect(self.func)

        button=QPushButton("CLOSE",self)                
        vBoxLayout.addWidget(button)
#        button.clicked.connect(self.CloseApp)
    
        
        grid_layout.addLayout(vBoxLayout, 0, 0)
        grid_layout.addWidget(self.pgcustom.win , 0, 1)
        grid_layout.addWidget(self.pgcustom2.win, 1, 0)
        grid_layout.addWidget(self.pgcustom3.win, 1, 1 )
        
class imagePlot(pg.ImageView):
    dp_input, image_header = load('DP_preprocessed.nii.gz')
    data = np.asarray(dp_input)

    # Interpret image data as row-major instead of col-major
    pg.setConfigOptions(imageAxisOrder='col-major')

    app = QtGui.QApplication([])
    
    # Create window with ImageView widget
    win = QtGui.QMainWindow()
    imv = pg.ImageView()
    win.setCentralWidget(imv)
    win.show()
    
    win.setWindowTitle('pyqtgraph example: ImageView')

    ## Display the data and assign each frame a time value from 1.0 to 3.0
    imv.setImage(data, xvals=np.linspace(1, 144, data.shape[0], dtype = 'int32'))
    ## Set a custom color map
    colors = [
        (0, 0, 0),
        (45, 5, 61),
        (84, 42, 55),
        (150, 87, 60),
        (208, 171, 141),
        (255, 255, 255)
    ]
    cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
    imv.setColorMap(cmap)
    imv.setCurrentIndex(72)
    imv.ui.roiBtn.hide()
    imv.ui.menuBtn.hide()


class imagePlot1(pg.ImageView):
    dp_input, image_header = load('DP_preprocessed.nii.gz')
    data = np.asarray(dp_input)

    # Interpret image data as row-major instead of col-major
    pg.setConfigOptions(imageAxisOrder='col-major')

    app = QtGui.QApplication([])
    
    # Create window with ImageView widget
    win = QtGui.QMainWindow()
    imv = pg.ImageView()
    win.setCentralWidget(imv)
    win.show()
    
    win.setWindowTitle('pyqtgraph example: ImageView')

    ## Display the data and assign each frame a time value from 1.0 to 3.0
    imv.setImage(data, xvals=np.linspace(1, 144, data.shape[0], dtype = 'int32'))
    ## Set a custom color map
    colors = [
        (0, 0, 0),
        (45, 5, 61),
        (84, 42, 55),
        (150, 87, 60),
        (208, 171, 141),
        (255, 255, 255)
    ]
    cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
    imv.setColorMap(cmap)
    imv.setCurrentIndex(72)
    imv.ui.roiBtn.hide()
    imv.ui.menuBtn.hide()

class imagePlot2(pg.ImageView):
    dp_input, image_header = load('DP_preprocessed.nii.gz')
    data = np.asarray(dp_input)

    # Interpret image data as row-major instead of col-major
    pg.setConfigOptions(imageAxisOrder='col-major')

    app = QtGui.QApplication([])
    
    # Create window with ImageView widget
    win = QtGui.QMainWindow()
    imv = pg.ImageView()
    win.setCentralWidget(imv)
    win.show()
    
    win.setWindowTitle('pyqtgraph example: ImageView')

    ## Display the data and assign each frame a time value from 1.0 to 3.0
    imv.setImage(data, xvals=np.linspace(1, 144, data.shape[0], dtype = 'int32'))
    ## Set a custom color map
    colors = [
        (0, 0, 0),
        (45, 5, 61),
        (84, 42, 55),
        (150, 87, 60),
        (208, 171, 141),
        (255, 255, 255)
    ]
    cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
    imv.setColorMap(cmap)
    imv.setCurrentIndex(72)
    imv.ui.roiBtn.hide()
    imv.ui.menuBtn.hide()

if __name__ == '__main__':
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
