import pandas as pd


class StochasticOscillator(object):
        
       """
       stochastic_oscillator compares where a securities price closed relative to it's price range over a given time period
       calculates Stochastic Oscillator indicators fastk(%K) and fastd(%D) for each span in a given span_list
       
       fastk(%K) -- closing price was above %K percent of all prior closings occuring in the past N periods. %K ranges (0%-100%)
       fastd(%D) -- 3 period simple moving average of %K
       
       span_list must contain list of day spans greater than or equal to 3 days
       """
    
    def __init__(self, data, span_list):
        super(StochasticOscillator, self).__init__()
        self.data = data['Ask_close']
        self.day_list = span_list
        self.stoch_data = pd.DataFrame()
        
    def calculate(self):
        for span in self.day_list:
            minute_span = span * 1440
            min_price = pd.rolling_min(self.data, minute_span, min_periods=1)    
            max_price = pd.rolling_max(self.data, minute_span, min_periods=1)
            fastk = 100 * ((self.data - min_price)/(max_price - min_price))                
            self.stoch_data[str(span) + 'Day %K'] = fastk
            fastd = pd.rolling_mean(fastk, 3*1440, min_periods=1)    # (3*1440) = number of minutes in 3 day period
            self.stoch_data[str(span) + 'Day %D'] = fastd
        return self.stoch_data
