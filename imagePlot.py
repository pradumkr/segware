# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 11:36:20 2019

@author: swati
"""
import pyqtgraph as pg
import numpy as np
import qtawesome as qta
from pyqtgraph.Qt import QtCore
from medpy.io import load

class imagePlot(pg.ImageView):
    
    def __init__(self, data):
        if data.any():
            self.data = data
        
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
            self.imv.setImage(self.data, xvals=np.linspace(1,self.data.shape[0] , self.data.shape[0], dtype = 'int32'))
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