# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 11:22:31 2019

@author: swati
"""

import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget)

import pyqtgraph as pg
import numpy as np

from pyqtgraph.Qt import QtCore
from medpy.io import load

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QGridLayout()
        grid.addWidget(self.createExampleGroup(), 0, 0)
        grid.addWidget(self.createExampleGroup1(), 0, 1)
        grid.addWidget(self.createExampleGroup1(), 1, 0)
        grid.addWidget(self.createExampleGroup1(), 1, 1)
        self.setLayout(grid)

        self.setWindowTitle("PyQt5 Group Box")
        self.resize(400, 300)

    def createExampleGroup(self):
        groupBox = QGroupBox("Controls")

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

        vBoxLayout.addStretch(1)
        groupBox.setLayout(vBoxLayout)

        return groupBox
    
    def createExampleGroup1(self):
        groupBox = QGroupBox("3D View")

        self.pgcustom = imagePlot()
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(self.pgcustom.imv)
#        vBoxLayout.addStretch(1)
        groupBox.setLayout(vBoxLayout)

        return groupBox
    
class imagePlot(pg.ImageView):
    
    def __init__(self):
        dp_input, image_header = load('DP_preprocessed.nii.gz')
        data = np.asarray(dp_input)
    
        # Interpret image data as row-major instead of col-major
        pg.setConfigOptions(imageAxisOrder='col-major')
        self.imv = pg.ImageView()
    
        ## Display the data and assign each frame a time value from 1.0 to 3.0
        self.imv.setImage(data, xvals=np.linspace(1, 144, data.shape[0], dtype = 'int32'))
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())