"""
@author: Eric Nelson
"""

from datamaker.feature import Feature

# pylint: disable=C0301

import pandas as pd
import numpy as np

class RollingPosition(Feature):
  """docstring for RollingPosition"""
  def __init__(self, span, lower, upper):
    super(RollingPosition, self).__init__()
    self.span = span
    self.lower = lower
    self.upper = upper

  def _calculate(self, data):
    """
    Calculate the mins and the maxs for the next "span" points
    for k candlestick,
      if k.high + upper < max.high && k.low - lower > min.low
        return 2, a strong buy
      elsif k.high + upper > max.high && k.low - lower < min.low
        return -2, a strong sell
      elsif k.high + upper < max.high && k.low - lower > min.low
        run through the data and see what is first
        for n in data[k+1:k+span]:
          if n.high > k.high + upper && n.low > k.low - lower
            return 1, # weak buy, the markey is very volatile
          elsif n.high < k.high + upper && n.low < k.low - lower
            return -1 # weak buy
          else
            return 0, # we can't know what was first, the market is too volatile
      else
        return 0

    """
    mins = pd.rolling_min(data["Bid_high"], self.span).shift(- self.span)
    maxs = pd.rolling_max(data["Bid_low"], self.span).shift(- self.span)
    o_data = pd.concat([data["Bid_low"], data["Bid_high"], mins, maxs], axis=1, keys=["low", "high", "min", "max"])

    result = np.empty(len(o_data))

    for index in range(len(o_data)):

      k = o_data.ix[index]

      if k["high"] + self.upper < k["max"] and k["low"] - self.lower > k["min"]:

        result[index] = 2

      elif k["high"] + self.upper > k["max"] and  k["low"] - self.lower < k["min"]:

        result[index] = -2

      elif k["high"] + self.upper < k["max"] and  k["low"] - self.lower < k["min"]:

        for offset in range(self.span):

          j = o_data.ix[max(index + offset, len(o_data)-1)]

          if   ((k["high"] + self.upper) < j["high"]) and ((k["low"] - self.lower) > j["low"]):

            result[index] = 1
            continue

          elif ((k["high"] + self.upper) > j["high"]) and ((k["low"] - self.lower) < j["low"]):

            result[index] = -1
            continue

          else:
            result[index] = 0
      else:
        result[index] = 0

    return result



