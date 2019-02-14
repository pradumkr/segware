import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow,QApplication,QDialog,QMessageBox,QVBoxLayout,QHBoxLayout,QGroupBox,QPushButton,QWidget
from PyQt5.QtCore import QCoreApplication

app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()

class Window(QDialog):    
    def __init__(self):
        super().__init__()
        self.title="PyQt5 layout"
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0,0,size.width(), size.height())#top,left,width,height

        self.VerticalLayout1()
        
        self.VerticalLayout2()
        
        hBox=QHBoxLayout()
        hBox.addWidget(self.groupbox1)
        hBox.addWidget(self.groupbox2)
        self.setLayout(hBox)
        self.show()

    def VerticalLayout1(self):
        self.groupbox1 =QGroupBox("part 1")
        vBoxLayout =QVBoxLayout()
        hBoxLayout=QHBoxLayout()
        button1=QPushButton("T1",self)
        vBoxLayout.addWidget(button1)
        button1.setToolTip("T1 ")

        button2=QPushButton("T2",self)
        vBoxLayout.addWidget(button2)
        
        button3=QPushButton("TC",self)
        vBoxLayout.addWidget(button3)

        button4=QPushButton("F",self)
        vBoxLayout.addWidget(button4)

        button5=QPushButton("SEGMENT",self)
        vBoxLayout.addWidget(button5)

        self.groupbox1.setLayout(vBoxLayout)


    def VerticalLayout2(self):
        self.groupbox2 =QGroupBox("part2")
        vBoxLayout =QVBoxLayout()
        hBoxLayout=QHBoxLayout()
        self.groupbox2.setLayout(vBoxLayout)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
