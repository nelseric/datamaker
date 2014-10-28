
"""
@author: Eric Nelson
"""

import pandas as pd

from datamaker.feature import Feature


class EWMA(Feature):
  """
    Calculates exponentially weighted moving average

    :param span: Span of EWMA in minutes
  """
  def __init__(self, span, *args, **kwargs):
    super(EWMA, self).__init__(*args, **kwargs)
    self.span = span

  def _calculate(self, data):
    result = pd.ewma(data, span=self.span)
    result.columns = [self.colname(col) for col in result.columns]

    return result

  def colname(self, col):
    """
    The column name for this indicator
    """
    return "EWMA{}_{}".format(self.span, col)


class NormalizedEWMA(Feature):
  """
    Calculates exponentially weighted moving average, and normalizes it.

    :param span: Span of EWMA in minutes
  """
  def __init__(self, span, *args, **kwargs):
    super(NormalizedEWMA, self).__init__(*args, **kwargs)
    self.span = span

  def _calculate(self, data):
    result = pd.ewma(data, span=self.span) - data
    result = pd.DataFrame(result)
    result.columns = [self.colname(col) for col in result.columns]

    return result

  def colname(self, col):
    """
    The column name for this indicator
    """
    return "NormalizedEWMA{}_{}".format(self.span, col)
