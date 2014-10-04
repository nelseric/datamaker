"""
 @author: Eric Nelson
"""

import pandas as pd
from datamaker.feature import Feature

class MACD(Feature):

  '''
    Calculates MACD values using several different EWMAs
    See http://en.wikipedia.org/wiki/MACD

    The default parameters represent the most common MACD, MACD(12,26,9)
    "As the working week used to be 6-days, the period settings of (12, 26, 9)
    represent 2 weeks, 1 month, and one and a half week."

    :param data: A dataframe, for which all columns will have the MACD
                 calculated
    :param fast_span: The short range EWMA span for use in MACD calculation
    :param slow_span: The long range EWMA span for use in MACD calculation
    :param signal_span: The medium range EWMA span that is compared to the
                        MACD to show divergance
  '''
  def __init__(self, *args, **kwargs):
    super(MACD, self).__init__(*args, **kwargs)
    self.fast_span = kwargs.get("fast_span", 12 * 1440)
    self.slow_span = kwargs.get("slow_span", 26 * 1440)
    self.signal_span = kwargs.get("signal_span", 9 * 1440)

  def calculate(self, data):
    """
      Calculates MACD using the configured parameters
    """
    fast_ewma = pd.ewma(data, span=self.fast_span)
    slow_ewma = pd.ewma(data, span=self.slow_span)

    macd = fast_ewma - slow_ewma
    signal = pd.ewma(macd, span=self.signal_span)
    divergance = macd - signal

    data = [macd, signal, divergance]
    keys = ["MACD", "Signal", "Divergance"]

    result = pd.concat(data, axis=1, keys=keys)

    result.columns = ['_'.join(col).strip() for col in result.columns.values]

    return result
