# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 17:23:48 2014

@author: alex lagerman
"""
import pandas as pd


class BollingerBands(object):
    
    #BollingerBands calculates 3 bands:
    #middle band = simple moving average of closing prices over period span
    #upper band = k standard deviations above middle band
    #lower band = k standard deviations below middle band
    #bandwidth = (upperband - lowerband)/middleband
    def __init__(self, data, span, k):
        super(BollingerBands, self).__init__()
        self.data = data['Ask_Close']
        self.day_span = span
        self.min_span = span * (1440)         #converts days to min: 1440min/day
        self.k = k
        self.bb_data = pd.DataFrame()
        
    def calculate(self):
        span_sma = pd.rolling_mean(self.data, self.min_span, min_periods=1)        
        span_std = self.k * pd.rolling_std(self.data, self.min_span, min_periods=1)
        self.bb_data[str(self.day_span) + 'Day MidBB'] = span_sma
        upperbb = span_sma + span_std
        self.bb_data[str(self.day_span) + 'Day UpperBB'] =  upperbb
        lowerbb = span_sma - span_std
        self.bb_data[str(self.day_span) + 'Day LowerBB'] = lowerbb
        self.bb_data[str(self.day_span) + 'Day Bandwidth'] = (upperbb - lowerbb)/span_sma
        return self.bb_data
