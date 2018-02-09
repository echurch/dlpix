from keras.layers import Input, merge, Dropout, Dense, Flatten, Activation
from keras.layers.convolutional import MaxPooling2D, Conv2D, MaxPooling3D
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.applications import vgg16 as vgg16loc

from keras import backend as K
from keras.utils.data_utils import get_file
from keras import optimizers as O
import numpy as np
import logging




class VGG16(Model):
  logger = logging.getLogger('pdk.vgg16')
  
  def __init__(self, generator):

    self.generator = generator
    self.logger.info("Assembling Model")

    x = generator.output

    self._input = Input(shape=x)

    self.logger.info(self._input.shape)
    import pdb

    # drop this to ~240x240 before even getting going, as a "sanity" check.
    layer = MaxPooling2D((1, 1), strides=(1, 1),  data_format='channels_first', 
                          name='block0_pool')(self._input)
    self.logger.info(layer.shape)

    K.set_image_data_format("channels_first")

#    layer = vgg16loc.VGG16(weights=None, include_top=False,input_shape=(self._input.shape[1].value,self._input.shape[2].value,self._input.shape[3].value))(self._input) 
    layer = vgg16loc.VGG16(weights=None, include_top=False,input_shape=(layer.shape[1].value,layer.shape[2].value,layer.shape[3].value))(layer)
    self.logger.info(layer.shape)

    
    # Classification block
    self.logger.info(layer.shape)
    layer = Flatten(name='flatten')(layer)
    #layer = Dense(4096, activation='relu', name='fc1')(layer)
    #layer = Dense(4096, activation='relu', name='fc2')(layer)
    layer = Dense(generator.input, activation='softmax', name='predictions')(layer)
    
    super(VGG16, self).__init__(self._input, layer)
    self.logger.info("Compiling Model")

    ogd = O.SGD(lr=0.01, decay=1e-6, momentum=0.3, nesterov=True)
    self.compile(loss='binary_crossentropy', optimizer=ogd, metrics=['categorical_accuracy'])

#    self.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
