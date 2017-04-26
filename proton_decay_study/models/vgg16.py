from keras.layers import Input, merge, Dropout, Dense, Flatten, Activation
from keras.layers.convolutional import MaxPooling3D, Conv3D, AveragePooling3D
from keras.layers.normalization import BatchNormalization
from keras.models import Model

from keras import backend as K
from keras.utils.data_utils import get_file
import logging


class VGG16(Model):
  logger = logging.getLogger('pdk.vgg16')
  
  def __init__(self, generator):

    self.generator = generator
    self.logger.info("Assembling Model")
    self._input = Input(shape=generator.output)
    self.logger.info(self._input.shape)

    layer = Conv3D(64, 3, activation='relu', padding='same', 
                          name='block1_conv1')(self._input)
    self.logger.info(layer.shape)
    layer = Conv3D(64, 3, activation='relu', padding='same', 
                          name='block1_conv2')(layer)
    self.logger.info(layer.shape)
    layer = MaxPooling3D((2, 1, 2), strides=(1, 2, 2), name='block1_pool')(layer)

    layer = Conv3D(128, 3, activation='relu', padding='same', 
                          name='block2_conv1')(layer)
    layer = Conv3D(128, 3, activation='relu', padding='same', 
                          name='block2_conv2')(layer)
    layer = MaxPooling3D((2, 1, 2), strides=(1, 2, 2), name='block2_pool')(layer)

    layer = Conv3D(256, 3, activation='relu', padding='same', 
                          name='block3_conv1')(layer)
    layer = Conv3D(256, 3, activation='relu', padding='same',
                          name='block3_conv2')(layer)
    layer = Conv3D(256, 3, activation='relu', padding='same', 
                          name='block3_conv3')(layer)
    layer = MaxPooling3D((2, 1, 2), strides=(1, 2, 2), name='block3_pool')(layer)

    layer = Conv3D(512, 3, activation='relu', padding='same', 
                          name='block4_conv1')(layer)
    layer = Conv3D(512, 3, activation='relu', padding='same', 
                          name='block4_conv2')(layer)
    layer = Conv3D(512, 3, activation='relu', padding='same', 
                          name='block4_conv3')(layer)
    layer = MaxPooling3D((2, 1, 2), strides=(1, 2, 2), name='block4_pool')(layer)

    layer = Conv3D(512, 3, activation='relu', padding='same', 
                          name='block5_conv1')(layer)
    layer = Conv3D(512, 3, activation='relu', padding='same', 
                          name='block5_conv2')(layer)
    layer = Conv3D(512, 3, activation='relu', padding='same', 
                          name='block5_conv3')(layer)
    layer = MaxPooling3D((2, 1, 2), strides=(1, 2, 2), name='block5_pool')(layer)

    # Classification block
    layer = Flatten(name='flatten')(layer)
    layer = Dense(4096, activation='relu', name='fc1')(layer)
    layer = Dense(4096, activation='relu', name='fc2')(layer)
    layer = Dense(generator.input, activation='softmax', name='predictions')(layer)
    
    super(VGG16, self).__init__(self._input, layer)
    self.logger.info("Compiling Model")
    self.compile(loss='binary_crossentropy', optimizer='sgd')
"""
  def train_with_incremental_save(self, samples_per_epoch, n_epochs_total, epoch_per_save):
    #loop over the trainings and save to file
    total_epoch



    training_output = model.fit_generator(self._input, samples_per_epoch = samples_per_epoch, 
                                      nb_epoch=n_epochs_total)
"""