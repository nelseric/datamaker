# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 17:23:48 2014

@author: alex lagerman
"""
import pandas as pd
import numpy as np


class Bollinger_Bands(object):
    
    #Calculates bollinger bands given span in days and k*stdev upper and lower bands (most common k=2)
    def __init__(self, data, span, k):
        super(Bollinger_Bands, self).__init__()
        self.data = data['Ask_Close']
        self.day_span = span
        self.min_span = span * (1440)         #converts days to min: 1440min/day
        self.k = k
        self.BB_Data = pd.DataFrame()
    def calcBands(self):
        #calculates simple moving average
        span_SMA = pd.rolling_mean(self.data, self.min_span, min_periods=1)        
        #calculates k *stdev
        span_STD = self.k * pd.rolling_std(self.data, self.min_span, min_periods=1)
        #middle band
        self.BB_Data[str(self.day_span) + 'Day MidBB'] = span_SMA 
        #upper band
        upperBB = span_SMA + span_STD
        self.BB_Data[str(self.day_span) + 'Day UpperBB'] =  upperBB
        #lower band
        lowerBB = span_SMA - span_STD
        self.BB_Data[str(self.day_span) + 'Day LowerBB'] = lowerBB
        #calculates Bandwidth
        self.BB_Data[str(self.day_span) + 'Day Bandwidth'] = (upperBB - lowerBB)/span_SMA
        return self.BB_Data
