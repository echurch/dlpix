from keras.layers import Input, merge, Dropout, Dense, Flatten, Activation
from keras.layers.convolutional import MaxPooling2D, Conv2D, MaxPooling3D
from keras.layers.normalization import BatchNormalization
from keras.models import Model

from keras import backend as K
from keras.utils.data_utils import get_file
from keras import optimizers as O
import logging


class VGG16(Model):
  logger = logging.getLogger('pdk.vgg16')
  
  def __init__(self, generator):

    self.generator = generator
    self.logger.info("Assembling Model")

    x = generator.output
    self._input = Input(shape=x)

    self.logger.info(self._input.shape)

    # drop this to ~240x240 before even getting going, as a "sanity" check.
    layer = MaxPooling2D((12, 16), strides=(12, 16),  data_format='channels_first', 
                          name='block0_pool')(self._input)
    self.logger.info(layer.shape)

    layer = Conv2D(32, 3, activation='relu', padding='same', data_format='channels_first',
                          name='block1_conv1')(layer)
    self.logger.info(layer.shape)
    layer = Conv2D(32, 3, activation='relu', padding='same', data_format='channels_first' ,
                          name='block1_conv2')(layer)
    self.logger.info(layer.shape)
    layer = MaxPooling2D((2, 2), strides=(2, 2),  data_format='channels_first',
                          name='block1_pool')(layer)
    self.logger.info(layer.shape)

    layer = Conv2D(64, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block2_conv1')(layer)
    self.logger.info(layer.shape)
    layer = Conv2D(64, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block2_conv2')(layer)
    self.logger.info(layer.shape)
    layer = MaxPooling2D((2, 2), strides=(2, 2),  data_format='channels_first', 
                          name='block2_pool')(layer)
    self.logger.info(layer.shape)
    layer = Conv2D(128, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block3_conv1')(layer)
    self.logger.info(layer.shape)
    layer = Conv2D(128, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block3_conv2')(layer)
    self.logger.info(layer.shape)
    layer = Conv2D(128, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block3_conv3')(layer)
    self.logger.info(layer.shape)
    layer = MaxPooling2D((2, 2), strides=(2, 2), data_format='channels_first',
                          name='block3_pool')(layer)

    self.logger.info(layer.shape)
    layer = Conv2D(256, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block4_conv1')(layer)
    self.logger.info(layer.shape)
    layer = Conv2D(256, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block4_conv2')(layer)
    self.logger.info(layer.shape)
    layer = Conv2D(256, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block4_conv3')(layer)
    self.logger.info(layer.shape)
    layer = MaxPooling2D((2, 2), strides=(2, 2), data_format='channels_first',
                          name='block4_pool')(layer)

    self.logger.info(layer.shape)
    layer = Conv2D(256, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block5_conv1')(layer)
    self.logger.info(layer.shape)
    layer = Conv2D(256, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block5_conv2')(layer)
    self.logger.info(layer.shape)
    layer = Conv2D(256, 3, activation='relu', padding='same',  data_format='channels_first',
                          name='block5_conv3')(layer)
    self.logger.info(layer.shape)
    layer = MaxPooling2D((2, 2), strides=(2, 2), data_format='channels_first',
                          name='block5_pool')(layer)

    # Classification block
    self.logger.info(layer.shape)
    layer = Flatten(name='flatten')(layer)
    layer = Dense(4096, activation='relu', name='fc1')(layer)
    #layer = Dense(4096, activation='relu', name='fc2')(layer)
    layer = Dense(generator.input, activation='softmax', name='predictions')(layer)
    
    super(VGG16, self).__init__(self._input, layer)
    self.logger.info("Compiling Model")

    ogd = O.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
    self.compile(loss='binary_crossentropy', optimizer=ogd, metrics=['categorical_accuracy'])

#    self.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
