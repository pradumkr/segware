import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QCoreApplication, QRect, Qt

app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()

class Window(QScrollArea):  
    def __init__(self):
        super().__init__()
        
        self.container = QFrame(self)
        
        self.container.resize(size.width(),size.height()/2)

        self.title="PyQt5 layout"
        self.setWindowTitle(self.title)
        self.setGeometry(0,0,size.width(), size.height()/2)#top,left,width,height

        hBox=QHBoxLayout(self.container)
        self.groupbox1 =QGroupBox("part 1")
        self.groupbox2 =QGroupBox("part 2")
        self.groupbox3 =QGroupBox("part 3")
        self.groupbox4 =QGroupBox("part 4")
        
        self.vBoxLayout =QVBoxLayout(self.container)
        self.vBoxLayout2 =QVBoxLayout(self.container)
        self.vBoxLayout3 =QVBoxLayout(self.container)
        self.vBoxLayout4 =QVBoxLayout(self.container)
        
        hBoxLayout=QHBoxLayout()

        #add buttons for part 1
        button1=QPushButton("T1",self)
        self.vBoxLayout.addWidget(button1)

        button2=QPushButton("T2",self)
        self.vBoxLayout.addWidget(button2)
        
        button3=QPushButton("TC",self)
        self.vBoxLayout.addWidget(button3)

        button4=QPushButton("F",self)
        self.vBoxLayout.addWidget(button4)

        button5=QPushButton("SEGMENT",self)
        self.vBoxLayout.addWidget(button5)
        button5.clicked.connect(self.func)

        button=QPushButton("CLOSE",self)                
        self.vBoxLayout.addWidget(button)
        button.clicked.connect(self.CloseApp)
    
        #add buttonfor part 2        
        button=QPushButton("A",self)
        self.vBoxLayout2.addWidget(button)

        #add for part 3
        button=QPushButton("1",self)
        self.vBoxLayout3.addWidget(button)

        #add for part 4
        
        button=QPushButton("c",self)
        self.vBoxLayout4.addWidget(button)


        #set layout position
        self.groupbox1.setLayout(self.vBoxLayout)
        hBox.addWidget(self.groupbox1)
        self.groupbox2.setLayout(self.vBoxLayout2)
        hBox.addWidget(self.groupbox2)
        self.groupbox3.setLayout(self.vBoxLayout3)
        self.groupbox4.setLayout(self.vBoxLayout4)
                
        self.setWidget(self.container)
        self.show()

    def func(self):
        self.container.resize(size.width(),size.height())
        self.vBoxLayout.addWidget(self.groupbox3)
        self.vBoxLayout2.addWidget(self.groupbox4)
    def CloseApp(self):
        reply = QMessageBox.question(self, "Close Message", "Are You Sure To Close Window",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
            
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
