import pandas as pd
import numpy as np
from datamaker.indicator import indicator as ai

class MACDIndicator(ai.Indicator):

  '''
    Calculates MACD values using most common spans
  '''
  def __init__(self, data):
    super(MACDIndicator, self).__init__(data)

  def calculate(self):
    self.macd = pd.ewma(self.data, span=12) - pd.ewma(self.data, span=26)
    self.signal = pd.ewma(self.data, span=9)
    self.divergance = self.macd - self.signal

  def result(self):
    return pd.concat([self.macd, self.signal, self.divergance], axis=1, keys=["MACD", "Signal", "Divergance"])
