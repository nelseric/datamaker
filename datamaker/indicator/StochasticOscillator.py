import pandas as pd


class Stochastic_Oscillator(object):

    #calculates Stochastic Oscillator indicators %K and %D for each span in a given span_list
    #span_list must contain list of day spans greater than or equal to 3 days
    def __init__(self, data, span_list):
        super(Stochastic_Oscillator, self).__init__()
        self.data = data['Ask_Close']
        self.day_list = span_list
        self.stoch_data = pd.DataFrame()
    def calc_stoch(self):
        for span in self.day_list:
            minute_span = span * 1440   #converts span in days to minutes
            min_price = pd.rolling_min(self.data, minute_span, min_periods=1)
            max_price = pd.rolling_max(self.data, minute_span, min_periods=1)
            percent_K = 100 * ((self.data - min_price)/(max_price - min_price))
            self.stoch_data[str(span) + 'Day %K'] = percent_K
            #calculates %D using 3day-period SMA of %K
            percent_D = pd.rolling_mean(percent_K, 3*1440, min_periods=1)    # (3*1440) = number of minutes in 3 day period
            self.stoch_data[str(span) + 'Day %D'] = percent_D
        return self.stoch_data
