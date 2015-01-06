import pandas as pd
from datamaker.feature import Feature


class StochasticOscillator(Feature):

    """
    stochastic_oscillator compares where a securities price closed relative to it's price range over a given time period
    calculates Stochastic Oscillator indicators fastk(%K) and fastd(%D) for each span in a given span_list
    fastk(%K) -- closing price was above %K percent of all prior closings occuring in the past N periods. %K ranges (0%-100%)
    fastd(%D) -- 3 period simple moving average of %K

    param: k_span: periods for fast_k span
    param: d_span: periods for sma in fast_d
    """

    def __init__(self, k_span=1000, d_span=3, *args, **kwargs):
        super(StochasticOscillator, self).__init__(*args, **kwargs)
        self.k_span = k_span
        self.d_span = d_span

    def _calculate(self, data):
        stoch_data = pd.DataFrame()
        min_price = pd.rolling_min(data, self.k_span, min_periods=1)
        max_price = pd.rolling_max(data, self.k_span, min_periods=1)
        fastk = 100 * ((data - min_price) / (max_price - min_price))
        stoch_data[str(self.k_span) + 'Period %K'] = fastk
        fastd = pd.rolling_mean(fastk, self.d_span, min_periods=1)
        stoch_data[str(self.k_span) + 'Period %D'] = fastd

        return stoch_data
