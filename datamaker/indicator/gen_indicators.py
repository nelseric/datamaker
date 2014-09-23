# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 23:44:48 2014

@author: alex
"""
import indicators
import pandas as pd


class GenIndicators(object):
    
    """
    Super class that calculates indicators using talib library
    Accepts 'ohlcv' pandas dataframe and a time period list
    time  period list must have units of minutes
    """
    
    def __init__(self, data, timeperiod):
        super(GenIndicators, self).__init__()
        self.data = {'open':   data['Open'],
                     'high':   data['High'],
                     'low':    data['Low'],
                     'close':  data['Close'],
                     'volume': data['Volume']}
        self.timeperiod = timeperiod
        
    def calculate(self):
        indicator_list = []
        
        adx = indicators.Adx(self.data, self.timeperiod).calculate()
        indicator_list.append(adx)
        
        adxr = indicators.Adxr(self.data, self.timeperiod).calculate()
        indicator_list.append(adxr)
        
        aroon = indicators.Aroon(self.data, self.timeperiod).calculate()
        indicator_list.append(aroon)
        
        aroonosc = indicators.Aroonosc(self.data, self.timeperiod).calculate()
        indicator_list.append(aroonosc)
        
        bop = indicators.Bop(self.data).calculate()
        indicator_list.append(bop)
        
        cci = indicators.Cci(self.data, self.timeperiod).calculate()
        indicator_list.append(cci)
        
        cmo = indicators.Cmo(self.data, self.timeperiod).calculate()
        indicator_list.append(cmo)
        
        macd = indicators.Macd(self.data, self.timeperiod).calculate()
        indicator_list.append(macd)
        
        mfi = indicators.Mfi(self.data, self.timeperiod).calculate()
        indicator_list.append(mfi)
        
        minusdi = indicators.Minus_DI(self.data, self.timeperiod).calculate()
        indicator_list.append(minusdi)
        
        mom = indicators.Mom(self.data, self.timeperiod).calculate()
        indicator_list.append(mom)
        
        ppo = indicators.Ppo(self.data, self.timeperiod).calculate()
        indicator_list.append(ppo)
        
        roc = indicators.Roc(self.data, self.timeperiod).calculate()
        indicator_list.append(roc)
        
        rocr = indicators.Rocr(self.data, self.timeperiod).calculate()
        indicator_list.append(rocr)
        
        rsi = indicators.Rsi(self.data, self.timeperiod).calculate()
        indicator_list.append(rsi)
        
        stoch = indicators.Stoch(self.data, self.timeperiod).calculate()
        indicator_list.append(stoch)

        stochf = indicators.StochF(self.data, self.timeperiod).calculate()
        indicator_list.append(stochf)
        
        stochrsi = indicators.StochRSI(self.data, self.timeperiod).calculate()
        indicator_list.append(stochrsi)
        
        ultosc = indicators.UltOSC(self.data, self.timeperiod).calculate()
        indicator_list.append(ultosc)
        
        willr = indicators.Willr(self.data, self.timeperiod).calculate()
        indicator_list.append(willr)
        
        atr = indicators.Atr(self.data, self.timeperiod).calculate()
        indicator_list.append(atr)
        
        trange = indicators.Trange(self.data).calculate()
        indicator_list.append(trange)
        
        ad = indicators.Ad(self.data).calculate()
        indicator_list.append(ad)
        
        adosc = indicators.Adosc(self.data, self.timeperiod).calculate()
        indicator_list.append(adosc)
        
        tsf = indicators.Tsf(self.data, self.timeperiod).calculate()
        indicator_list.append(tsf)
        
        indicator_data = pd.concat(indicator_list, axis=1)
        return indicator_data