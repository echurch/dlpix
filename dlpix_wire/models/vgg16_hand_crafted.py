from keras.layers import Input, merge, Dropout, Dense, Flatten, Activation
from keras.layers.convolutional import MaxPooling2D, Conv2D, MaxPooling3D
from keras.layers.normalization import BatchNormalization
from keras.models import Model

from keras import backend as K
from keras.utils.data_utils import get_file
from keras import optimizers as O
import logging


class VGG16_hand_crafted(Model):
  logger = logging.getLogger('pixgen.vgg16')
  
  def __init__(self, generator):

    self.generator = generator
    self.logger.info("Assembling Model")

    x = generator.output
    self._input = Input(shape=x)

    import pdb

    self.logger.info(self._input.shape)

    # Could drop this to ~240x240 before even getting going, as a "sanity" check.
    
    layer = MaxPooling2D((2, 2), strides=(2, 2),  data_format='channels_first', 
                          name='block0_pool')(self._input)
    self.logger.info(layer.shape)

    
    layer = Conv2D(64, (3,3) , activation='relu', padding='same', data_format='channels_first',
                          name='block1_conv1')(layer)

    layer = Conv2D(64, (3,3), activation='relu', padding='same', data_format='channels_first' ,
                          name='block1_conv2')(layer)

    layer = MaxPooling2D((2, 2), strides=(2, 2),  data_format='channels_first',
                          name='block1_pool')(layer)
    self.logger.info(layer.shape)
    

    
    
    
    self.logger.info(layer.shape)
    layer = Conv2D(256, (3,3), activation='relu', padding='same',  data_format='channels_first',
                          name='block3_conv1')(layer)


    layer = Conv2D(256, (3,3), activation='relu', padding='same',  data_format='channels_first',
                          name='block3_conv2')(layer)

    layer = Conv2D(256, (3,3), activation='relu', padding='same',  data_format='channels_first',
                          name='block3_conv3')(layer) 

    layer = MaxPooling2D((3, 3), strides=(3, 3), data_format='channels_first',
                          name='block3_pool')(layer)
    self.logger.info(layer.shape)
    '''


    layer = Conv2D(512, (3,3), activation='relu', padding='same',  data_format='channels_first',
                          name='block4_conv1')(layer)
    self.logger.info(layer.shape)
    layer = Conv2D(512, (3,3), activation='relu', padding='same',  data_format='channels_first',
                          name='block4_conv2')(layer)
    self.logger.info(layer.shape)

    layer = Conv2D(512, (3,3), activation='relu', padding='same',  data_format='channels_first',
                          name='block4_conv3')(layer)
    self.logger.info(layer.shape)

    layer = MaxPooling2D((2, 2), strides=(2, 2), data_format='channels_first',
                          name='block4_pool')(layer)

    self.logger.info(layer.shape)
    layer = Conv2D(512, (3,3), activation='relu', padding='same',  data_format='channels_first',
                          name='block5_conv1')(layer)
    self.logger.info(layer.shape)
    layer = Conv2D(512, (3,3), activation='relu', padding='same',  data_format='channels_first',
                          name='block5_conv2')(layer)
    self.logger.info(layer.shape)

    '''
    layer = Conv2D(512, (15,15), activation='relu', padding='same',  data_format='channels_first',
                          name='block5_conv3')(layer)

    layer = MaxPooling2D((15, 15), strides=(15, 15), data_format='channels_first',
                          name='block5_pool')(layer)

    # Classification block
    self.logger.info(layer.shape)
    layer = Flatten(name='flatten')(layer)
    layer = Dense(4096, activation='relu', name='fc1')(layer)
    layer = Dense(4096, activation='relu', name='fc2')(layer)
    layer = Dense(generator.input, activation='softmax', name='predictions')(layer)
    
    super(VGG16_hand_crafted, self).__init__(self._input, layer)
    self.logger.info("Compiling Model")

    ogd = O.SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)

#    ogd = O.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)  # some argument not liked here. EC 24-Jan-2018
    self.compile(loss='binary_crossentropy', optimizer=ogd, metrics=['categorical_accuracy'])

#    self.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
