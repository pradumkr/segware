# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 22:54:12 2019

@author: swati
"""

from __future__ import absolute_import
from __future__ import print_function

from keras.layers import Input, concatenate, Conv2D, MaxPooling2D, Activation,Conv2DTranspose, UpSampling2D, BatchNormalization, add
from keras.layers.core import Flatten, Reshape
from keras.models import Model
from keras.regularizers import l2
import keras.backend as K
from keras.layers.advanced_activations import ELU, LeakyReLU
from keras.utils import plot_model
from keras.layers.core import Dropout
import tensorflow as tf

import os
os.environ["PATH"] += os.pathsep + 'C:/Users/lokes/Anaconda3/envs/tensorflow/Library/bin/graphviz/'

def _shortcut(input, residual):
    """Adds a shortcut between input and residual block and merges them with "sum"
    """
    # Expand channels of shortcut to match residual.
    # Stride appropriately to match residual (width, height)
    # Should be int if network architecture is correctly configured.
    input_shape = K.int_shape(input)
    residual_shape = K.int_shape(residual)
    stride_width = int(round(input_shape[1] / residual_shape[1]))
    stride_height = int(round(input_shape[2] / residual_shape[2]))
    equal_channels = input_shape[3] == residual_shape[3]

    shortcut = input
    # 1 X 1 conv if shape is different. Else identity.
    if stride_width > 1 or stride_height > 1 or not equal_channels:
        shortcut = Conv2D(filters=residual_shape[3],
                          kernel_size=(1, 1),
                          strides=(stride_width, stride_height),
                          padding="valid",
                          kernel_initializer="he_normal",
                          kernel_regularizer=l2(0.0001))(input)

    res  = add([shortcut, residual])
    return ELU()(res)
 

def encoder_block(input_tensor, m, n):
    x = BatchNormalization()(input_tensor)
    x = Activation('relu')(x)
#    x = lrelu(x)
    x = Conv2D(filters=n, kernel_size=(3, 3), strides=(2, 2), padding="same")(x)

    x = BatchNormalization()(x)
    x = Activation('relu')(x)
#    x = lrelu(x)
    x = Conv2D(filters=n, kernel_size=(3, 3), padding="same")(x)

    added_1 = _shortcut(input_tensor, x)

    x = BatchNormalization()(added_1)
    x = Activation('relu')(x)
#    x = lrelu(x)
    x = Conv2D(filters=n, kernel_size=(3, 3), padding="same")(x)

    x = BatchNormalization()(x)
    x = Activation('relu')(x)
#    x = lrelu(x)
    x = Conv2D(filters=n, kernel_size=(3, 3), padding="same")(x)

    added_2 = _shortcut(added_1, x)

    return added_2

def decoder_block(input_tensor, m, n):
    x = BatchNormalization()(input_tensor)
    x = Activation('relu')(x)
#    x = lrelu(x)
    x = Conv2D(filters=int(m/4), kernel_size=(1, 1))(x)

    x = UpSampling2D((2, 2))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
#    x = lrelu(x)
    x = Conv2D(filters=int(m/4), kernel_size=(3, 3), padding='same')(x)

    x = BatchNormalization()(x)
    x = Activation('relu')(x)
#    x = lrelu(x)
    x = Conv2D(filters=n, kernel_size=(1, 1))(x)

    return x

def LinkNet(input_shape=(256, 256, 3), classes=2):
    inputs = Input(shape=input_shape)

    x = BatchNormalization()(inputs)
    x = Activation('relu')(x)
#    x = lrelu(x)
    x = Conv2D(filters=64, kernel_size=(7, 7), strides=(2, 2))(x)

    x = MaxPooling2D((3, 3), strides=(2, 2), padding="same")(x)

    encoder_1 = encoder_block(input_tensor=x, m=64, n=64)
    encoder_1 = Dropout(0.2)(encoder_1)
    
    encoder_2 = encoder_block(input_tensor=encoder_1, m=64, n=128)
    encoder_2 = Dropout(0.2)(encoder_2)
    
    encoder_3 = encoder_block(input_tensor=encoder_2, m=128, n=256)
    encoder_3 = Dropout(0.2)(encoder_3)

    encoder_4 = encoder_block(input_tensor=encoder_3, m=256, n=512)
    encoder_4 = Dropout(0.2)(encoder_4)

    decoder_4 = decoder_block(input_tensor=encoder_4, m=512, n=256)
    decoder_4 = Dropout(0.2)(decoder_4)

    decoder_3_in = concatenate([decoder_4, encoder_3])
    decoder_3_in = Activation('relu')(decoder_3_in)
#    decoder_3_in = lrelu(decoder_3_in)
    decoder_3 = decoder_block(input_tensor=decoder_3_in, m=256, n=128)
    decoder_3 = Dropout(0.2)(decoder_3)
    

    decoder_2_in = concatenate([decoder_3, encoder_2])
    decoder_2_in = Activation('relu')(decoder_2_in)
#    decoder_2_in = lrelu(decoder_2_in)
    
    decoder_2 = decoder_block(input_tensor=decoder_2_in, m=128, n=64)
    decoder_2 = Dropout(0.2)(decoder_2)

    decoder_1_in = concatenate([decoder_2, encoder_1])
    decoder_1_in = Activation('relu')(decoder_1_in)
#    decoder_1_in = lrelu(decoder_1_in)
    
    decoder_1 = decoder_block(input_tensor=decoder_1_in, m=64, n=64)
    decoder_1 = Dropout(0.2)(decoder_1)

    x = UpSampling2D((2, 2))(decoder_1)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
#    x = lrelu(x)
    x = Conv2D(filters=32, kernel_size=(3, 3), padding="same")(x)

    x = BatchNormalization()(x)
    x = Activation('relu')(x)
#    x = lrelu(x)
    x = Conv2D(filters=32, kernel_size=(3, 3), padding="same")(x)

    x = UpSampling2D((2, 2))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
#    x = lrelu(x)
    
    x = Conv2D(filters=classes, kernel_size=(2, 2), padding="same")(x)
    output = Reshape([-1, classes])(x)
    output = Activation('softmax')(output)
    x = Reshape(input_shape[:-1] + (classes,))(output)

    model = Model(inputs=inputs, outputs=x)
    return model

#lnet = LinkNet(input_shape=(240, 240, 2))
#lnet.summary()
#plot_model(lnet, to_file='model_mlinknet.png')
#
#y_pred = model.predict(X_e[260:280] , batch_size = 1, verbose = 0, steps = None)
#
#imshow(X_e[80,:,:,0])
#imshow(Y_e[279,:,:,0])
#imshow(pred_2[19,:,:,0])
#pred_2 = (y_pred > 0.5).astype(int)

