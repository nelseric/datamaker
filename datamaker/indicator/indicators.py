# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 13:36:52 2014

@author: alex

"""

from talib.abstract import *
import pandas as pd

"""
Contains all subclasses for individual indicator calculations
"""

class Adx(object):
    
    def __init__(self, data, timeperiod_list):
        super(Adx, self).__init__()
        self. data = data
        self.timeperiod_list = timeperiod_list
        self.adx_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.adx_data[str(timeperiod) + 'Min ADX'] = ADX(self.data, timeperiod)
        return self.adx_data
      
      
class Adxr(object):
    
    def __init__(self, data, timeperiod_list):
        super(Adxr, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.adxr_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.adxr_data[str(timeperiod) + 'Min ADXR'] = ADXR(self.data, timeperiod)
        return self.adxr_data
        
        
class Aroon(object):
    
    def __init__(self, data, timeperiod_list):
        super(Aroon, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.aroon_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            aroondown, aroonup = AROON(self.data, timeperiod)
            self.aroon_data[str(timeperiod) + 'Min Aroondown'] = aroondown
            self.aroon_data[str(timeperiod) + 'Min Aroonup'] = aroonup
        return self.aroon_data
        
        
class Aroonosc(object):
    
    def __init__(self, data, timeperiod_list):
        super(Aroonosc, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.aroonosc_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.aroonosc_data[str(timeperiod) + 'Min Aroonosc'] = AROONOSC(self.data, timeperiod)
        return self.aroonosc_data
        
        
class Bop(object):
    
    def __init__(self, data):
        super(Bop, self).__init__()
        self.data = data
        self.bop_data = pd.DataFrame()
        
    def calculate(self):
        self.bop_data['BOP'] = BOP(self.data)
        return self.bop_data
       

class Cci(object):
    
    def __init__(self, data, timeperiod_list):
        super(Cci, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.cci_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.cci_data[str(timeperiod) + 'Min CCI'] = CCI(self.data, timeperiod)
        return self.cci_data
        
        
class Cmo(object):
    
    def __init__(self, data, timeperiod_list):
        super(Cmo, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.cmo_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.cmo_data[str(timeperiod) + 'Min CMO'] = CMO(self.data, timeperiod)
        return self.cmo_data
        
        
class Macd(object):
    
    def __init__(self, data, timeperiod_list):
        super(Macd, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.macd_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            macd, macdsignal, macdhist = MACD(self.data, 12*timeperiod, 26*timeperiod, 9*timeperiod)
            self.macd_data[str(timeperiod) + 'Min MACD'] = macd
            self.macd_data[str(timeperiod) + 'Min MACD Signal'] = macdsignal
            self.macd_data[str(timeperiod) + 'Min MACD Hist'] = macdhist
        return self.macd_data
        
        
class Mfi(object):
    
    def __init__(self, data, timeperiod_list):
        super(Mfi, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.mfi_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.mfi_data[str(timeperiod) + 'Min MFI'] = MFI(self.data, timeperiod)
        return self.mfi_data
        
        
class Minus_DI(object):
    
    def __init__(self, data, timeperiod_list):
        super(Minus_DI, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.minusdi_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.minusdi_data[str(timeperiod) + 'Min MINUS_DI'] = MINUS_DI(self.data, timeperiod)
        return self.minusdi_data


class Mom(object):
    
    def __init__(self, data, timeperiod_list):
        super(Mom, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.mom_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.mom_data[str(timeperiod) + 'Min MOM'] = MOM(self.data, timeperiod)
        return self.mom_data
        

class Ppo(object):
    
    def __init__(self, data, timeperiod_list):
        super(Ppo, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.ppo_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.ppo_data['Min PPO'] = PPO(self.data, 9*timeperiod, 26*timeperiod, 1)
        return self.ppo_data


class Roc(object):
    
    def __init__(self, data, timeperiod_list):
        super(Roc, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.roc_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.roc_data[str(timeperiod) + 'Min ROC'] = ROC(self.data, timeperiod)
        return self.roc_data


class Rocr(object):
    
    def __init__(self, data, timeperiod_list):
        super(Rocr, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.rocr_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.rocr_data[str(timeperiod) + 'Min ROCR'] = ROCR(self.data, timeperiod)
        return self.rocr_data


class Rsi(object):
    
    def __init__(self, data, timeperiod_list):
        super(Rsi, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.rsi_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.rsi_data[str(timeperiod) + 'Min RSI'] = RSI(self.data, timeperiod)
        return self.rsi_data


class Stoch(object):
    
    def __init__(self, data, timeperiod_list):
        super(Stoch, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.stoch_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            slowk, slowd = STOCH(self.data, timeperiod, 3, 0, 3, 0)
            self.stoch_data[str(timeperiod) + 'Min SLOWK'] = slowk
            self.stoch_data[str(timeperiod) + 'Min SLOWD'] = slowd
        return self.stoch_data
        
        
class StochF(object):
    
    def __init__(self, data, timeperiod_list):
        super(StochF, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.stochf_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            fastk, fastd = STOCHF(self.data, timeperiod, 3, 0)
            self.stochf_data[str(timeperiod) + 'Min FASTK'] = fastk
            self.stochf_data[str(timeperiod) + 'Min FASTD'] = fastd
        return self.stochf_data
        

class StochRSI(object):
    
    def __init__(self, data, timeperiod_list):
        super(StochRSI, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.stochrsi_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            fastk, fastd = STOCHRSI(self.data, timeperiod, 5, 3, 0)
            self.stochrsi_data[str(timeperiod) + 'Min FASTK'] = fastk
            self.stochrsi_data[str(timeperiod) + 'Min FASTD'] = fastd
        return self.stochrsi_data
        
        
class UltOSC(object):
    def __init__(self, data, timeperiod_list):
        super(UltOSC, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.ultosc_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            timeperiod2 = timeperiod * 2
            timeperiod3 = timeperiod2 * 2
            ultosc = ULTOSC(self.data, timeperiod, timeperiod2, timeperiod3)
            self.ultosc_data[str(timeperiod) + 'Min ULTOSC'] = ultosc
        return self.ultosc_data
        

class Willr(object):
    
    def __init__(self, data, timeperiod_list):
        super(Willr, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.willr_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.willr_data[str(timeperiod) + 'Min WILLR'] = WILLR(self.data, timeperiod)
        return self.willr_data


class Atr(object):
    
    def __init__(self, data, timeperiod_list):
        super(Atr, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.atr_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.atr_data[str(timeperiod) + 'Min ATR'] = ATR(self.data, timeperiod)
        return self.atr_data
        

class Trange(object):
    
    def __init__(self, data):
        super(Trange, self).__init__()
        self.data = data
        self.trange_data = pd.DataFrame()
        
    def calculate(self):
        self.trange_data['TRANGE'] = TRANGE(self.data)
        return self.trange_data
        

class Tsf(object):
    
    def __init__(self, data, timeperiod_list):
        super(Tsf, self).__init__()
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.tsf_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            self.tsf_data[str(timeperiod) + 'Min TSF'] = TSF(self.data, timeperiod)
        return self.tsf_data
        

class Ad(object):
    
    def __init__(self, data):
        super(Ad, self).__init__()
        self.data = data
        self.ad_data = pd.DataFrame()
        
    def calculate(self):
        self.ad_data['Chaikin A/D Line'] = AD(self.data)
        return self.ad_data
        

class Adosc(object):
    
    def __init__(self, data, timeperiod_list):
        self.data = data
        self.timeperiod_list = timeperiod_list
        self.adosc_data = pd.DataFrame()
        
    def calculate(self):
        for timeperiod in self.timeperiod_list:
            fastperiod = timeperiod
            slowperiod = fastperiod * 3
            self.adosc_data[str(timeperiod) + 'Min ADOSC'] = ADOSC(self.data, fastperiod, slowperiod)
        return self.adosc_data