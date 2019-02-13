from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget, QAction, QMessageBox, QPushButton
import sys
app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Application_name"
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.InitWindow()


    def InitWindow(self):

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
        
        button1 =QPushButton("T1",self)
        button1.move(50,100)
        button1.setToolTip("T1 ")

        button2 =QPushButton("T2",self)
        button2.move(50,150)
        button2.setToolTip("T2 ")

        button3 =QPushButton("TC",self)
        button3.move(50,200)
        button3.setToolTip("This will ")
        
        button4 =QPushButton("F",self)
        button4.move(50,250)
        button4.setToolTip("This will ")

        button = QPushButton("close",self)
        button.move(50,350)
        button.setToolTip("This will close")
        button.clicked.connect(self.close)

        button4 =QPushButton("Segment",self)
        button4.move(50,300)
        button4.setToolTip("This will ")

        self.setWindowTitle(self.title)
        self.setGeometry(0,0,size.width(), size.height())#top,left,width,height
        self.show()

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

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())
