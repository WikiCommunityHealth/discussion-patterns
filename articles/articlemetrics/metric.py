from abc import ABC, abstractmethod

class Metric(ABC):

  @abstractmethod
  def reset(self):
    pass

  @abstractmethod
  def calculate(self):
    pass
