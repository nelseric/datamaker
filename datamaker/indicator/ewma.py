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

    def calculate(self):
        self._result = pd.ewma(self.data, span=self.span)

class NormalizedEWMA(Feature):
    """
      Calculates exponentially weighted moving average, and normalizes it.

      :param span: Span of EWMA in minutes
    """
    def __init__(self, span, *args, **kwargs):
        super(NormalizedEWMA, self).__init__(*args, **kwargs)
        self.span = span

    def calculate(self):
        self._result = pd.ewma(self.data, span=self.span) - self.data
