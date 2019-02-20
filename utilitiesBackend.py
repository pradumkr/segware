# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 12:45:40 2019

@author: swati
"""
import os, glob, h5py
from time import time
import numpy as np
import cv2
from medpy.io import load
from Models.LinknetTumor import *
from Models.IResUnetBrainFluids import *
from skimage.io import imshow


#t1, _ = load('S:\\Our Projects and Papers\\Neonatal Brain MRI Segmentation Using Deep Concatenated Residual Learning\\Datasets\\iSeg-2017-Training\\subject-3-T1.img')
#t2, _ = load('S:\\Our Projects and Papers\\Neonatal Brain MRI Segmentation Using Deep Concatenated Residual Learning\\Datasets\\iSeg-2017-Training\\subject-3-T2.img')
#o, _ = load('S:\\Our Projects and Papers\\Neonatal Brain MRI Segmentation Using Deep Concatenated Residual Learning\\Datasets\\iSeg-2017-Training\\subject-3-label.img')
#o[o == 10] = 1 
#o[o == 150] = 2
#o[o == 250] = 3 
#o = o[np.newaxis,:,:,:]

class BrainFluids():
    def __init__(self, t1, t2):
        self.t1 = t1[np.newaxis,:,:,:]
        self.t2 = t2[np.newaxis,:,:,:]
        self.prepX()
        
    def label_to_one_hot_encode(self, patches_label):
    #    patches_label = total_aug_prep_label
        csf = ((patches_label == 1).astype(int))
        print(csf.shape)
        csf = csf[:,:,:,:,np.newaxis]
        gm = ((patches_label == 2).astype(int))
        gm = gm[:,:,:,:,np.newaxis]
        wm = ((patches_label == 3).astype(int))
        wm = wm[:,:,:,:,np.newaxis]
        bg = ((patches_label == 0).astype(int))
        bg = bg[:,:,:,:,np.newaxis]
        
        c = np.concatenate([csf, gm, wm, bg], axis = -1)
        return c
    
    def prepX(self):
        self.prep_t1 = []
        self.prep_t2 = []
        
        for j in range(len(self.t1)):
            img_t1 = self.t1[j,:,:,:]
            pixels_t1 = img_t1[img_t1 > 0]
            mean_t1 = pixels_t1.mean()
            std_t1  = pixels_t1.std()
            norm_img_t1 = (img_t1 - mean_t1)/std_t1
            print(mean_t1, std_t1)
            print(norm_img_t1.min(), norm_img_t1.max())
            print(img_t1.min(), img_t1.max())
            self.prep_t1.append(norm_img_t1)
            
            img_t2 = self.t2[j,:,:,:]
            pixels_t2 = img_t2[img_t2 > 0]
            mean_t2 = pixels_t2.mean()
            std_t2  = pixels_t2.std()
            norm_img_t2 = (img_t2 - mean_t2)/std_t2
            print(mean_t2, std_t2)
            print(norm_img_t2.min(), norm_img_t2.max())
            print(img_t2.min(), img_t2.max())
            self.prep_t2.append(norm_img_t2)
            
        self.t1 = np.asarray(self.prep_t1)
        self.t2 = np.asarray(self.prep_t2)

    def loadModelAndPredictAll(self):
        self.model = get_segment_model((48,64,64,2))
        self.model.load_weights('./Models/modelBrainFluids.h5')
        self.predict()
        
    def predict(self):
        t1_test, t2_test = self.t1[0:1], self.t2[0:1]
        t = time()
        self.y_pred = np.zeros([t1_test.shape[0], 144, 192, 256, 4])
        
        for n in range(t1_test.shape[0]):
            for i in range(3):
                for j in range(3):
                    for k in range(4):
                        xt1 = t1_test[n, i*48:(i+1)*48, j*64:(j+1)*64, k*64:(k+1)*64]
                        xt2 = t2_test[n, i*48:(i+1)*48, j*64:(j+1)*64, k*64:(k+1)*64]
                        xt1 = xt1[np.newaxis,:,:,:,np.newaxis]
                        xt2 = xt2[np.newaxis,:,:,:,np.newaxis]
                        x = np.concatenate([xt1, xt2], axis = -1)
                        self.y_pred[n, i*48:(i+1)*48, j*64:(j+1)*64, k*64:(k+1)*64, :] = self.model.predict(x, batch_size = 1, verbose = 0, steps = None)
            print("------"+ str(n) + "-----------")
        t1 = time()
        print(t1-t)
#        return self.y_pred
        
    def predictCSF(self):
        self.csf_pred = self.y_pred[:,:,:,:,0]
        self.csf_pred = (self.csf_pred > 0.35).astype('int')
        return self.csf_pred
        
    def predictGM(self):
        self.gm_pred = self.y_pred[:,:,:,:,1]
        self.gm_pred = (self.gm_pred > 0.65).astype('int')
        return self.gm_pred
        
    def predictWM(self):
        self.wm_pred = self.y_pred[:,:,:,:,2]
        self.wm_pred = (self.wm_pred > 0.20).astype('int')
        return self.wm_pred

#b = BrainFluids(t1, t2)
#b.loadModel()
#y = b.predict()

#t1, _ = load('./sampleData/Tumor/t1.mha')
#t2, _ = load('./sampleData/Tumor/t2.mha')
#t1c, _ = load('./sampleData/Tumor/t1c.mha')
#f, _ = load('./sampleData/Tumor/flair.mha')
#o, _ = load('./sampleData/Tumor/mask.mha')
        
class Tumor():
    def __init__(self, t1, t2, t1c, f):
        print(t1.shape)
        self.t1 = self.normalize(t1)[:,:,11:145]
        self.t2 = self.normalize(t2)[:,:,11:145]
        self.t1c = self.normalize(t1c)[:,:,11:145]
        self.f = self.normalize(f)[:,:,11:145]
        self.t1 = np.transpose(self.t1, (2, 0, 1))
        self.t2 = np.transpose(self.t2, (2, 0, 1))
        self.t1c = np.transpose(self.t1c, (2, 0, 1))
        self.f = np.transpose(self.f, (2, 0, 1))
        print(self.t1.shape)
        self.resizeAndPrepX()
        
    def normalize(self, cube):
        pixels = cube[cube > 0]
        mean = pixels.mean()
        std = pixels.std()
        norm = (cube - mean) / std
        return norm
    
    def resizeAndPrepX(self):
        self.X = []   
        print("***", self.f.shape)
        for j in range(len(self.f)):
            f_n = np.insert(self.f[j], 240, self.f[j,232:240,:], axis = 1)
            f_n = np.insert(f_n, 0, f_n[232:240,:240], axis = 1)
            f_n = np.insert(f_n, 0, f_n[232:240,:], axis = 0)
            f_n = np.insert(f_n, 240, f_n[232:240,:], axis = 0)
            
            t1_n = np.insert(self.t1[j], 240, self.t1[j,232:240,:], axis = 1)
            t1_n = np.insert(t1_n, 0, t1_n[232:240,:240], axis = 1)
            t1_n = np.insert(t1_n, 0, t1_n[232:240,:], axis = 0)
            t1_n = np.insert(t1_n, 240, t1_n[232:240,:], axis = 0)
            
            t1c_n = np.insert(self.t1c[j], 240, self.t1c[j,232:240,:], axis = 1)
            t1c_n = np.insert(t1c_n, 0, t1c_n[232:240,:240], axis = 1)
            t1c_n = np.insert(t1c_n, 0, t1c_n[232:240,:], axis = 0)
            t1c_n = np.insert(t1c_n, 240, t1c_n[232:240,:], axis = 0)
            
            t2_n = np.insert(self.t2[j], 240, self.t2[j,232:240,:], axis = 1)
            t2_n = np.insert(t2_n, 0, t2_n[232:240,:240], axis = 1)
            t2_n = np.insert(t2_n, 0, t2_n[232:240,:], axis = 0)
            t2_n = np.insert(t2_n, 240, t2_n[232:240,:], axis = 0)
            
            f_n = f_n[:,:,np.newaxis]
            t1_n = t1_n[:,:,np.newaxis]
            t1c_n = t1c_n[:,:,np.newaxis]
            t2_n = t2_n[:,:,np.newaxis]
            
            x = np.concatenate([f_n, t1_n, t1c_n, t2_n], axis=-1)
            
            self.X.append(x)
        
        self.X = np.asarray(self.X) # (134, 256, 256, 4)
        print(self.X.shape)
        
    def loadModel(self):
        self.model = LinkNet(input_shape = (256,256,4))
        self.model.load_weights('./Models/modelTumor.h5')
        
    def predict(self):
        self.y_pred = self.model.predict(self.X , batch_size = 1, verbose = 0, steps = None)
        self.y_pred = self.y_pred[:,8:248,8:248]
        pad1 = np.zeros((11, 240,240,2))
        pad2 = np.zeros((10, 240,240,2))
        self.y_pred = np.concatenate((pad1, self.y_pred, pad2), axis=0)
        self.y_pred = (self.y_pred > 0.7).astype(int)
        return self.y_pred

#t = Tumor(t1, t2, t1c, f)
#t.loadModel()
#y = t.predict()
