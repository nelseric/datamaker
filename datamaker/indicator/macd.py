import pandas as pd
import numpy as np

class MACDIndicator(object):

  '''Calculates MACD values using most common spans'''
  def __init__(self, data):
    super(MACDIndicator, self).__init__()
    self.data = data
    self.macd = pd.ewma(self.data, span=12) - pd.ewma(self.data, span=26)
    self.signal = pd.ewma(self.data, span=9)
    self.divergance = self.macd - self.signal

  def combine(self):
    return pd.concat([self.macd, self.signal, self.divergance], axis=1, keys=["MACD", "Signal", "Divergance"])
