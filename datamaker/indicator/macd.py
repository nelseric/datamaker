import pandas as pd
import numpy as np
from datamaker.feature import Feature

class MACDIndicator(Feature):

  '''
    Calculates MACD values using several different EWMAs
    See http://en.wikipedia.org/wiki/MACD

    The default parameters represent the most common MACD, MACD(12,26,9)
    "As the working week used to be 6-days, the period settings of (12, 26, 9) represent 2 weeks, 1 month, and one and a half week."

    :param data: A dataframe, for which all columns will have the MACD calculated
    :param fast_span: The short range EWMA span for use in MACD calculation
    :param slow_span: The long range EWMA span for use in MACD calculation
    :param signal_span: The medium range EWMA span that is compared to the MACD to show divergance
  '''
  def __init__(self, data, fast_span = 12 * 1440, slow_span = 26 * 1440, signal_span = 9 * 1440):
    super(MACDIndicator, self).__init__(data)
    self.fast_span = fast_span
    self.slow_span = slow_span
    self signal_span = signal_span

  def calculate(self):
    self.macd = pd.ewma(self.data, span = self.fast_span) - pd.ewma(self.data, span = self.slow_span)
    self.signal = pd.ewma(self.macd, span = self.signal_span)
    self.divergance = self.macd - self.signal

    self._result = pd.concat([self.macd, self.signal, self.divergance], axis=1, keys=["MACD", "Signal", "Divergance"])
