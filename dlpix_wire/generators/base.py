import logging
from abc import abstractmethod, ABCMeta


class BaseDataGenerator(object, metaclass=ABCMeta):
  """
    Base data generator which hooks into the networks to provide
    an interface to the incoming data.
  """
  logger = logging.getLogger('pdk.generator')

  def __init__(self):
    self._dataset = None

  def __len__(self):
    return len(self._dataset)

  def __iter__(self):
    return self

  def __next__(self):
    return next(self)

  @abstractmethod
  def next(self):
    raise StopIteration()
