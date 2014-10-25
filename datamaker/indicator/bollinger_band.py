# -*- coding: utf-8 -*- 
"""
Created on Thu Sep  4 17:23:48 2014

@author: alex lagerman, Eric Nelson
"""
import pandas as pd

from datamaker.feature import Feature

class BollingerBand(Feature):
  """
  BollingerBands calculates 3 bands:
  middle band -- simple moving average of closing prices over period span
  upper band -- k standard deviations above middle band
  lower band -- k standard deviations below middle band
  bandwidth -- (upperband - lowerband)/middleband

  :param period: The period of the BB in minutes, defaults is 20 dats
  :param k: The number of std deviations to add or subtract to form the BB
  """
       
  def __init__(self, period=28800, k=2, *args, **kwargs):
    super(BollingerBand, self).__init__(*args, **kwargs)
    self.period = period
    self.k = k
    self._label = "BBp_{}_k{}_".format(self.period, self.k)

  def _calculate(self, data):
    """
      Calculate the Bollinger Band
    """

    moving_avg = pd.rolling_mean(data, self.period, min_periods=1)        
    k_stdev = self.k * pd.rolling_std(data, self.period, min_periods=1)


    lowerbb = moving_avg - k_stdev
    upperbb = moving_avg + k_stdev
    bandwidth = (upperbb - lowerbb)/moving_avg

    indicators = [moving_avg, upperbb, lowerbb, bandwidth]
    keys = ["SMA", "UpperBB", "LowerBB", "Bandwidth"]
    keys = [self._label + label for label in keys]

    result = pd.concat(indicators, axis=1, keys=keys)

    result.columns = [''.join(col).strip() for col in result.columns.values]

    return result
   
