"Buy Strategy"

from datamaker.strategy import Strategy

class Naive(Strategy):
  """docstring for Naive"""
  def __init__(self, arg):
    super(Naive, self).__init__()
    self.arg = arg
  

  def get_prediction(self):
    True