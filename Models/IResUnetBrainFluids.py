# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 01:51:49 2019

@author: swati
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 09:00:25 2018

@author: swati
"""

from keras.models import Model
from keras import backend as K
from keras.optimizers import Adadelta
from keras.utils import multi_gpu_model
from keras.models import model_from_json
from keras.layers import Input, Conv3D, Convolution3D, Dense, UpSampling3D, Activation, MaxPooling3D, Dropout, Reshape, Activation, Flatten, Multiply, Subtract
from keras.layers.merge import concatenate
from keras.layers.normalization import BatchNormalization
import numpy as np
from keras.layers import Concatenate, Lambda
from keras.utils import plot_model
from keras.layers.advanced_activations import ELU, LeakyReLU
import os
os.environ["PATH"] += os.pathsep + 'C:/Users/swati/Anaconda3/envs/tensorflow/Library/bin/graphviz/'

def res_block(inputs, filters, kernel_size = 1 , scale = 0.1):
    residual = Convolution3D(padding='same', filters=filters, kernel_size = 1)(inputs)
    residual = BatchNormalization()(residual)
    residual = Lambda(lambda x: x*scale)(residual)
    res = concatenate([inputs, residual])
    return ELU()(res) 

def get_segment_model(inp_shape, k_size=2):
    
    merge_axis = -1 # Feature maps are concatenated along last axis (for tf backend)
    data = Input(shape=inp_shape)
    conv11 = Convolution3D(padding='same', filters=32, kernel_size = 1)(data)
    conv11 = Activation('relu')(conv11)
    conv11 = BatchNormalization()(conv11)
    conv11 = Convolution3D(padding='same', filters=32, kernel_size = 3)(conv11)
    conv11 = BatchNormalization()(conv11)
    conv11 = Activation('relu')(conv11)
    
    conv12 = Convolution3D(padding='same', filters=32, kernel_size = 1)(data)
    conv12 = BatchNormalization()(conv12)
    conv12 = Activation('relu')(conv12)
    conv12 = Convolution3D(padding='same', filters=32, kernel_size = 5)(conv12)
    conv12 = BatchNormalization()(conv12)
    conv12 = Activation('relu')(conv12)
    
    conv13 = MaxPooling3D((3, 3, 3), strides = (1, 1, 1), padding = 'same')(data)
    conv13 = Convolution3D(padding='same', filters=32, kernel_size = 1)(conv13)
    conv13 = BatchNormalization()(conv13)
    conv13 = Activation('relu')(conv13)
    
    conv14 = Convolution3D(padding='same', filters=32, kernel_size = 1)(data)
    conv14 = BatchNormalization()(conv14)
    conv14 = Activation('relu')(conv14)
    
    conv2 = concatenate([conv11, conv12, conv13, conv14], axis=-1)
    pool1 = MaxPooling3D(pool_size=(2, 2, 2))(conv2)
    pool1 = Dropout(0.2)(pool1)

#    ------------------------------------------------------------------------------------------

    conv3 = Convolution3D(padding='same', filters=64, kernel_size=k_size)(pool1)
    conv3 = BatchNormalization()(conv3)
    conv3 = Activation('relu')(conv3)
    conv4 = Convolution3D(padding='same', filters=64, kernel_size=k_size)(conv3)
    conv4 = BatchNormalization()(conv4)
    conv4 = Activation('relu')(conv4)
    pool2 = MaxPooling3D(pool_size=(2, 2, 2))(conv4)
    pool2 = Dropout(0.2)(pool2)
    
#    ------------------------------------------------------------------------------------------
    
    conv51 = Convolution3D(padding='same', filters=128, kernel_size = 1)(pool2)
    conv51 = Activation('relu')(conv51)
    conv51 = BatchNormalization()(conv51)
    conv51 = Convolution3D(padding='same', filters=128, kernel_size = 3)(conv51)
    conv51 = BatchNormalization()(conv51)
    conv51 = Activation('relu')(conv51)
    
    conv52 = Convolution3D(padding='same', filters=128, kernel_size = 1)(pool2)
    conv52 = BatchNormalization()(conv52)
    conv52 = Activation('relu')(conv52)
    conv52 = Convolution3D(padding='same', filters=128, kernel_size = 5)(conv52)
    conv52 = BatchNormalization()(conv52)
    conv52 = Activation('relu')(conv52)
    
    conv53 = MaxPooling3D((3, 3, 3), strides = (1, 1, 1), padding = 'same')(pool2)
    conv53 = Convolution3D(padding='same', filters=128, kernel_size = 1)(conv53)
    conv53 = BatchNormalization()(conv53)
    conv53 = Activation('relu')(conv53)
    
    conv54 = Convolution3D(padding='same', filters=128, kernel_size = 1)(pool2)
    conv54 = BatchNormalization()(conv54)
    conv54 = Activation('relu')(conv54)
    
    conv6 = concatenate([conv51, conv52, conv53, conv54], axis = -1)
    pool3 = MaxPooling3D(pool_size=(2, 2, 2))(conv6)
    pool3 = Dropout(0.2)(pool3)

#    ------------------------------------------------------------------------------------------------
    conv7 = Convolution3D(padding='same', filters=256, kernel_size=k_size)(pool3)
    conv7 = BatchNormalization()(conv7)
    conv7 = Activation('relu')(conv7)
    conv8 = Convolution3D(padding='same', filters=256, kernel_size=k_size)(conv7)
    conv8 = BatchNormalization()(conv8)
    conv8 = Activation('relu')(conv8)
    pool4 = MaxPooling3D(pool_size=(2, 2, 2), padding="same")(conv8)
    pool4 = Dropout(0.2)(pool4)
    
    
    
    conv10 = Convolution3D(padding='same', filters=512, kernel_size=k_size)(pool4)
    conv10 = BatchNormalization()(conv10)
    conv11 = Activation('relu')(conv10)
    conv11 = Dropout(0.2)(conv11)
    
    up1 = UpSampling3D(size=(2, 2, 2))(conv11)
    conv12 = Convolution3D(padding='same', filters=256, kernel_size=k_size)(up1)
    conv12 = BatchNormalization()(conv12)
    conv12 = Activation('relu')(conv12)
    conv13 = Convolution3D(padding='same', filters=256, kernel_size=k_size)(conv12)
    conv13 = BatchNormalization()(conv13)
    conv13 = Activation('relu')(conv13)
    res1 = res_block (conv8, 256)
    merged1 = concatenate([conv13, res1], axis=merge_axis)
    
    convup11 = Convolution3D(padding='same', filters=256, kernel_size = 1)(merged1)
    convup11 = Activation('relu')(convup11)
    convup11 = BatchNormalization()(convup11)
    convup11 = Convolution3D(padding='same', filters=256, kernel_size = 3)(convup11)
    convup11 = BatchNormalization()(convup11)
    convup11 = Activation('relu')(convup11)
    
    convup12 = Convolution3D(padding='same', filters=256, kernel_size = 1)(merged1)
    convup12 = BatchNormalization()(convup12)
    convup12 = Activation('relu')(convup12)
    convup12 = Convolution3D(padding='same', filters=256, kernel_size = 5)(convup12)
    convup12 = BatchNormalization()(convup12)
    convup12 = Activation('relu')(convup12)
    
    convup13= MaxPooling3D((3, 3, 3), strides = (1, 1, 1), padding = 'same')(merged1)
    convup13 = Convolution3D(padding='same', filters=256, kernel_size = 1)(convup13)
    convup13= BatchNormalization()(convup13)
    convup13= Activation('relu')(convup13)
    
    convup14 = Convolution3D(padding='same', filters=256, kernel_size = 1)(merged1)
    convup14 = BatchNormalization()(convup14)
    convup14 = Activation('relu')(convup14)
    
    conv14 = concatenate([convup11, convup12, convup13, convup14], axis=-1)
    poolup1 = BatchNormalization()(conv14)
    poolup1 = Activation('relu')(poolup1)
    poolup1 = Dropout(0.2)(poolup1)

    up2 = UpSampling3D(size=(2, 2, 2))(poolup1)
    conv15 = Convolution3D(padding='same', filters=128, kernel_size=k_size)(up2)
    conv15 = BatchNormalization()(conv15)
    conv15 = Activation('relu')(conv15)
    conv16 = Convolution3D(padding='same', filters=128, kernel_size=k_size)(conv15)
    conv16 = BatchNormalization()(conv16)
    conv16 = Activation('relu')(conv16)
    res2 = res_block (conv6, 128)
    merged2 = concatenate([conv16, res2], axis=merge_axis)
    conv17 = Convolution3D(padding='same', filters=128, kernel_size=k_size)(merged2)
    conv17 = BatchNormalization()(conv17)
    conv17 = Activation('relu')(conv17)
    conv17 = Dropout(0.2)(conv17)

    up3 = UpSampling3D(size=(2, 2, 2))(conv17)
    conv18 = Convolution3D(padding='same', filters=64, kernel_size=k_size)(up3)
    conv18 = BatchNormalization()(conv18)
    conv18 = Activation('relu')(conv18)
    conv19 = Convolution3D(padding='same', filters=64, kernel_size=k_size)(conv18)
    conv19 = BatchNormalization()(conv19)
    conv19 = Activation('relu')(conv19)
    res3 = res_block (conv4, 64)
    merged3 = concatenate([conv19, res3], axis=merge_axis)
    
    convup21 = Convolution3D(padding='same', filters=64, kernel_size = 1)(merged3)
    convup21 = Activation('relu')(convup21)
    convup21 = BatchNormalization()(convup21)
    convup21 = Convolution3D(padding='same', filters=64, kernel_size = 3)(convup21)
    convup21 = BatchNormalization()(convup21)
    convup21 = Activation('relu')(convup21)
    
    convup22 = Convolution3D(padding='same', filters=64, kernel_size = 1)(merged3)
    convup22 = BatchNormalization()(convup22)
    convup22 = Activation('relu')(convup22)
    convup22 = Convolution3D(padding='same', filters=64, kernel_size = 5)(convup22)
    convup22 = BatchNormalization()(convup22)
    convup22 = Activation('relu')(convup22)
    
    convup23= MaxPooling3D((3, 3, 3), strides = (1, 1, 1), padding = 'same')(merged3)
    convup23 = Convolution3D(padding='same', filters=64, kernel_size = 1)(convup23)
    convup23= BatchNormalization()(convup23)
    convup23= Activation('relu')(convup23)
    
    convup24 = Convolution3D(padding='same', filters=64, kernel_size = 1)(merged3)
    convup24 = BatchNormalization()(convup24)
    convup24 = Activation('relu')(convup24)
    
    conv20 = concatenate([convup21, convup22, convup23, convup24], axis=-1)
    poolup2 = BatchNormalization()(conv20)
    poolup2 = Activation('relu')(poolup2)
    poolup2 = Dropout(0.2)(poolup2)

    up4 = UpSampling3D(size=(2, 2, 2))(poolup2)
    conv21 = Convolution3D(padding='same', filters=32, kernel_size=k_size)(up4)
    conv21 = BatchNormalization()(conv21)
    conv21 = Activation('relu')(conv21)
    conv22 = Convolution3D(padding='same', filters=32, kernel_size=k_size)(conv21)
    conv22 = BatchNormalization()(conv22)
    conv22 = Activation('relu')(conv22)
    res4 = res_block (conv2, 32)
    merged4 = concatenate([conv22, res4], axis=merge_axis)
    conv23 = Convolution3D(padding='same', filters=32, kernel_size=k_size)(merged4)
    conv23 = BatchNormalization()(conv23)
    conv23 = Activation('relu')(conv23)
    conv23 = Dropout(0.2)(conv23)

    conv24 = Convolution3D(padding='same', filters=4, kernel_size=k_size)(conv23)
    output = Reshape([-1, 4])(conv24)
    output = Activation('softmax')(output)
    
#    output = Activation('sigmoid')(output)
    
    output = Reshape(inp_shape[:-1] + (4,))(output)

    model = Model(data, output)
    
    
    return model

#m = get_segment_model((48,64,64,2))
#plot_model(m, to_file='model_inet.png')



