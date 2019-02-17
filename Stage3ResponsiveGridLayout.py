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

# setimage.axes -> transform (coronal, saggital, transverse)
# setcurrentindex for slider value update   
#    http://www.pyqtgraph.org/documentation/graphicsItems/viewbox.html#pyqtgraph.ViewBox.setMouseEnabled
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window_widget = Grid(parent=self)
        
        self.window_widget.installEventFilter(self)
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
        
    def eventFilter(self, obj, event):
        if event.type() in (QtCore.QEvent.MouseButtonPress,QtCore.QEvent.MouseButtonDblClick):
            if(event.button() == QtCore.Qt.RightButton):
                print("Right button clicked")
                return True;
        return super(MainWindow, self).eventFilter(obj, event)

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
    
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setMinimum(0)
        self.slider.setMaximum(144)
        self.slider.setValue(0)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.slider_value_changed)
#        vBoxLayout.addWidget(self.slider)
        
        self.nameLabel = QLabel("Current Slice : ")
        self.nameLabel.setMaximumHeight(20)
        vBoxLayout.addWidget(self.nameLabel)
        
        self.slice_box = QSpinBox()
        self.slice_box.setRange(0,144)
        self.slice_box.valueChanged.connect(self.slice_box_value_changed)
        slider_layout = QGridLayout()
        slider_layout.addWidget(self.slider, 0,0,1,4);
        slider_layout.addWidget(self.slice_box,0,4,1,1);
        
        vBoxLayout.addLayout(slider_layout)
        
        grid_layout.addLayout(vBoxLayout, 0, 0)
        grid_layout.addWidget(self.pgcustom.win , 0, 1)
        grid_layout.addWidget(self.pgcustom2.win, 1, 0)
        grid_layout.addWidget(self.pgcustom3.win, 1, 1 )
    
    def slider_value_changed(self):
        print(str(self.slider.value()))
        self.slice_box.setValue(self.slider.value())
        self.nameLabel.setText("Current Slice: " +str(self.slider.value()))
        self.pgcustom.setCurrentIndex(self.slider.value())
        
    def slice_box_value_changed(self):
        print(str(self.slice_box.value()))
        self.slider.setValue(self.slice_box.value())
        self.nameLabel.setText("Current Slice: " +str(self.slider.value()))
        self.pgcustom.setCurrentIndex(self.slider.value())
        
        
        
class imagePlot(pg.ImageView):
    dp_input, image_header = load('DP_preprocessed.nii.gz')
    data = np.asarray(dp_input)
#    data = np.transpose(data,(0,2,1))

    # Interpret image data as row-major instead of col-major
    pg.setConfigOptions(imageAxisOrder='col-major')

    app = QtGui.QApplication([])
    
    # Create window with ImageView widget
    win = QtGui.QMainWindow()
    imv = pg.ImageView()
    
#    imv.view.setLimits(maxXRange = data.shape[1], maxYRange= data.shape[2])
#    imv.view.setAspectLocked(lock=False, ratio=2 )
#    imv.autoRange()
    win.setCentralWidget(imv)
    imv.view.setBackgroundColor('#f0f0f0')
    imv.timeLine.setPen('y', width=10)
    imv.ui.splitter.setChildrenCollapsible(False)
    imv.ui.splitter.setStretchFactor(8,1)
    imv.timeLine.setHoverPen('r', width=12)
    imv.view.setMenuEnabled(False)  
    roi = imv.getRoiPlot()
    slider = roi.plotItem.getViewWidget()
    slider.setMaximumHeight(60)
    roi.plotItem.setMenuEnabled(False)
#    imv.ui.splitter.setCollapsible(2,False)
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
    
    def 


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
