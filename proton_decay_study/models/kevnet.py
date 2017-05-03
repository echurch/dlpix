from keras.layers import Input, merge, Dropout, Dense, Flatten, Activation
from keras.layers.convolutional import MaxPooling3D, Conv3D
from keras.layers.normalization import BatchNormalization
from keras.models import Model

from keras import backend as K
from keras.utils.data_utils import get_file

import tensorflow as tf
import logging


class Kevnet(Model):
  logger = logging.getLogger('pdk.kevnet')
  
  def __init__(self, generator):

    self.generator = generator
    self.logger.info("Assembling Model")
    self._input = Input(shape=generator.output)
    self.logger.info(self._input)
    self.logger.info(self._input.shape)

    # First block (atomic block)

    layer = Conv3D(2, (1,9,5), strides=(1,9,5), 
                   activation='relu', padding='same', 
                   data_format='channels_first',
                   name='block1_conv1')(self._input)
    self.logger.info(layer.shape)
    layer = MaxPooling3D((1, 2, 2), strides=(1,2, 2),  
                          data_format='channels_first', 
                          name='block1_pool')(layer)
    self.logger.info(layer.shape)
    layer = BatchNormalization(axis=2, name="block1_norm")(layer)
    self.logger.info(layer.shape)

    """
    layer = Conv3D(32, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block2_conv1')(self._input)
    self.logger.info(layer.shape)
    layer = MaxPooling3D((1, 2, 2), strides=(1,2, 2),  data_format='channels_first', name='block2_pool')(layer)
    self.logger.info(layer.shape)
    layer = BatchNormalization(axis=2, name="block1_norm")(layer)
    self.logger.info(layer.shape)
    """

    # Classification block
    #self.logger.info(layer.shape)
    layer = Flatten(name='flatten')(layer)
    #layer = Dense(1024, activation='relu', name='fc1')(layer)
    layer = Dense(256, activation='relu', name='fc2')(layer)
    layer = Dense(generator.input, activation='softmax', name='predictions')(layer)
    self.logger.info(layer.shape)

    super(Kevnet, self).__init__(self._input, layer)
    self.logger.info("Compiling Model")
    self.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])





    



