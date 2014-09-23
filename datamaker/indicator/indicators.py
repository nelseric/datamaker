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

    """
    Average Directional Movement Index (ADX) is an indicator of trend strength
    in a series of prices.
    ADX is a lagging indicator and will rang between 0-100
    ADX < 20 indicates trend weakness
    ADX > 40 indicates trend strength
    ADX > 50 indicates an extremely strong trend
    """

    def __init__(self, data, timeperiod):
        super(Adx, self).__init__()
        self. data = data
        self.timeperiod = timeperiod
        self.adx_data = pd.DataFrame()

    def calculate(self):
        adx = ADX(self.data, self.timeperiod)
        self.adx_data[str(self.timeperiod) + 'Min ADX'] = adx
        return self.adx_data
      
      
class Adxr(object):

    """
    The Average Directional Movement Index Rating (ADXR) measures the strength of the ADX
    ADXR(i) = (ADX(i) + ADX(i-n))/2 where n = ADXR interval
    ADXR ranges from 0-100
    lower values reflect weak trend
    higher values reflect strong trend
    Helps better display trends in volatile markets
    """

    def __init__(self, data, timeperiod):
        super(Adxr, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.adxr_data = pd.DataFrame()
        
    def calculate(self):
        adxr = ADXR(self.data, self.timeperiod)
        self.adxr_data[str(self.timeperiod) + 'Min ADXR'] = adxr
        return self.adxr_data
        
        
class Aroon(object):

    """
    The Aroon indicator is used to identify trends and likelihood that trends will reverse
    Made up of two lines:
        -Aroonup: measures strength of an upward trend
        -Aroondown: measures strength of a downward trend
    Each line reports a percentage of total time it takes for the price to reach the highest and lowest
    points over a given time period and ranges from 0-100%, 0 being weak trend, and 100 being strong trend
    """

    def __init__(self, data, timeperiod):
        super(Aroon, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.aroon_data = pd.DataFrame()
        
    def calculate(self):
        aroondown, aroonup = AROON(self.data, self.timeperiod)
        self.aroon_data[str(self.timeperiod) + 'Min Aroondown'] = aroondown
        self.aroon_data[str(self.timeperiod) + 'Min Aroonup'] = aroonup
        return self.aroon_data
        
        
class Aroonosc(object):

    """
    The Aroon Oscillator(AROONOSC uses Aroonup and Aroondown to gauge the strength of a current trend
    and the likelihood that it will continue.
    AROONOSC = Aroonup - Aroondown
    AROONOSC > 0 indicates uptrend is present
    AROONOSC < 0 indicates a downtrend is present
    """

    def __init__(self, data, timeperiod):
        super(Aroonosc, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.aroonosc_data = pd.DataFrame()
        
    def calculate(self):
        aroonosc = AROONOSC(self.data, self.timeperiod)
        self.aroonosc_data[str(self.timeperiod) + 'Min AROONOSC'] = aroonosc
        return self.aroonosc_data
        
        
class Bop(object):

    """
    The Balance of Power (BOP) measures the strength of the bulls vs. the bears by assessing
    the ability of each to push price to extreme levels
    Balance Power = (Close - Open)/(High - Low)
    Balance of Power (BOP) = SMA(Balance Power)
    BOP > 0 indicates buy signal, Increasing BOP indicates upward trend
    BOP < 0 indicates sell signal, Decreasing BOP indicates downward trend
    """

    def __init__(self, data):
        super(Bop, self).__init__()
        self.data = data
        self.bop_data = pd.DataFrame()
        
    def calculate(self):
        self.bop_data['BOP'] = BOP(self.data)
        return self.bop_data
       

class Cci(object):

    """
    The Commodity Channel Inex (CCI) quantifies the relationship between the assets price,
    a moving average(SMA) of the assets price and normal deviations(D) from that average.
    CCI = (PRICE - SMA) / (.015 * D)
    Sell Signal:
        CCI > 100 and started to trend downwards
    Buy Signal:
        CCI < -100 and started to trend upwards
    """

    def __init__(self, data, timeperiod):
        super(Cci, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.cci_data = pd.DataFrame()
        
    def calculate(self):
        cci = CCI(self.data, self.timeperiod)
        self.cci_data[str(self.timeperiod) + 'Min CCI'] = cci
        return self.cci_data
        
        
class Cmo(object):

    """
    The Chande Momentum Oscillator (CMO)
    S(u) - Sum of difference between todays close and yesterdays close
    S(d) - Absolute Value of the difference between todays close and yesterdays close
    CMO = ( S(u) - S(d) ) / ( S(u) + S(d) ) * 100
    CMO range (-100,+100)
    CMO > +50 indicates overbought
    CMO < -50 indicates oversold
    """

    def __init__(self, data, timeperiod):
        super(Cmo, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.cmo_data = pd.DataFrame()

    def calculate(self):
        cmo = CMO(self.data, self.timeperiod)
        self.cmo_data[str(self.timeperiod) + 'Min CMO'] = cmo
        return self.cmo_data
        
        
class Macd(object):

    """
    Calculates MACD indicator using common timeperiod intervals.
    """

    def __init__(self, data, timeperiod):
        super(Macd, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.macd_data = pd.DataFrame()
        
    def calculate(self):
        macd, macdsignal, macdhist = MACD(self.data, 12*self.timeperiod, 26*self.timeperiod, 9*self.timeperiod)
        self.macd_data[str(self.timeperiod) + 'Min MACD'] = macd
        self.macd_data[str(self.timeperiod) + 'Min MACD Signal'] = macdsignal
        self.macd_data[str(self.timeperiod) + 'Min MACD Hist'] = macdhist
        return self.macd_data
        
        
class Mfi(object):

    """
    Money Flow Index (MFI) uses stocks price and volume to predict the reliability of current trend.
    1. Typical Price = (High + Low + Close)/3
    2. Raw Money Flow = Typical Price * Volume
    3. Money Flow Ratio = (N-Period Positive Money Flow)/(N-Period Negative Money Flow)
        - Positive Money Flow - sum of typical price over N periods
          created when typical price is greater than previous typical price.
        - Negative Money Flow - Sum of typical price over N periods
          created when typical price is less than previous typical price
    4. Money Flow Index (MFI) = 100 - [100/(1 + Money Flow Ratio)]
    """

    def __init__(self, data, timeperiod):
        super(Mfi, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.mfi_data = pd.DataFrame()
        
    def calculate(self):
        mfi = MFI(self.data, self.timeperiod)
        self.mfi_data[str(self.timeperiod) + 'Min MFI'] = mfi
        return self.mfi_data
        
        
class Minus_DI(object):

    """
    The Negative Directional Indicator is used to measure the presence of a downtrend
    MINUS_DI sloping upward indicates the strength of downtrend is increasing
    """

    def __init__(self, data, timeperiod):
        super(Minus_DI, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.minusdi_data = pd.DataFrame()
        
    def calculate(self):
        minusdi = MINUS_DI(self.data, self.timeperiod)
        self.minusdi_data[str(self.timeperiod) + 'Min MINUS_DI'] = minusdi
        return self.minusdi_data


class Mom(object):

    """
    The Momentum Indicator is used to measure the velocity of price change
    MOM = Current_Close Price - N-Period Ago Close Price
    Values will produce line indicating whether prices are rising or falling over N-period
    """

    def __init__(self, data, timeperiod):
        super(Mom, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.mom_data = pd.DataFrame()
        
    def calculate(self):
        mom = MOM(self.data, self.timeperiod)
        self.mom_data[str(self.timeperiod) + 'Min MOM'] = mom
        return self.mom_data
        

class Ppo(object):

    """
    Percentage Price Oscillator (PPO) shows relationship among two moving averages
    Result is a percentage revealing where short term average is relative to long term average
    A PPO of 10 means the short term average is 10% above the long term average
    """

    def __init__(self, data, timeperiod):
        super(Ppo, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.ppo_data = pd.DataFrame()
        
    def calculate(self):
        ppo = PPO(self.data, 9*self.timeperiod, 26*self.timeperiod, 1)
        self.ppo_data[str(self.timeperiod) + 'Min PPO'] = ppo
        return self.ppo_data


class Roc(object):

    """
    Rate of Change:
    A technical indicator that measures the percentage change between the most recent price and the
    price "n" periods in the past.
    It is calculated by using the following formula:
    (Closing Price Today - Closing Price "n" Periods Ago) / Closing Price "n" Periods Ago

    ROC is classed as a price momentum indicator or a velocity indicator because
    it measures the rate of change or the strength of momentum of change.
    """

    def __init__(self, data, timeperiod):
        super(Roc, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.roc_data = pd.DataFrame()
        
    def calculate(self):
        roc = ROC(self.data, self.timeperiod)
        self.roc_data[str(self.timeperiod) + 'Min ROC'] = roc
        return self.roc_data


class Rocr(object):

    """
    Rate of Change Ratio indicates the rate of change as a ratio over N-periods
    """

    def __init__(self, data, timeperiod):
        super(Rocr, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.rocr_data = pd.DataFrame()
        
    def calculate(self):
        rocr = ROCR(self.data, self.timeperiod)
        self.rocr_data[str(self.timeperiod) + 'Min ROCR'] = rocr
        return self.rocr_data


class Rsi(object):

    """
    Relative Strength Index (RSI) compares the magnitude of recent gains to recent losses
    to determine overbought and oversold conditions.
    RSI = 100 - 100/(1 + RS)
    RS = Average of N period up closes / Average of N periods down closes
    RSI ranges from 0-100
    RSI >= 70 indicates overbought
    RSI <= 30 indicates oversold
    """

    def __init__(self, data, timeperiod):
        super(Rsi, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.rsi_data = pd.DataFrame()
        
    def calculate(self):
        rsi = RSI(self.data, self.timeperiod)
        self.rsi_data[str(self.timeperiod) + 'Min RSI'] = rsi
        return self.rsi_data


class Stoch(object):

    """
    Stochastic Oscillator compares closing price to a price range over an N-period of time
    In an upward trending market prices tend to close near their high
    In a downward trending market prices tend to close near their low
    A transaction signal occurs when slowk and slowd cross
    """

    def __init__(self, data, timeperiod):
        super(Stoch, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.stoch_data = pd.DataFrame()
        
    def calculate(self):
        slowk, slowd = STOCH(self.data, self.timeperiod, 3, 0, 3, 0)
        self.stoch_data[str(self.timeperiod) + 'Min SLOWK'] = slowk
        self.stoch_data[str(self.timeperiod) + 'Min SLOWD'] = slowd
        return self.stoch_data
        
        
class StochF(object):

    """
    Stochastic Oscillator Fast is similar to Stochastic Oscillator but is more
    sensitive to changing prices.
    Transaction signal occurs when fastk and fastd cross
    """

    def __init__(self, data, timeperiod):
        super(StochF, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.stochf_data = pd.DataFrame()
        
    def calculate(self):
        fastk, fastd = STOCHF(self.data, self.timeperiod, 3, 0)
        self.stochf_data[str(self.timeperiod) + 'Min FASTK'] = fastk
        self.stochf_data[str(self.timeperiod) + 'Min FASTD'] = fastd
        return self.stochf_data
        

class StochRSI(object):

    """
    Stochastic Relative Strength Index takes the Stochastic Oscillator of RSI values
    Ranges between 0 and 1
    STOCHRSI < 0.20 indicates oversold
    STOCHRSI > 0.80 indicates overbought
    """

    def __init__(self, data, timeperiod):
        super(StochRSI, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.stochrsi_data = pd.DataFrame()
        
    def calculate(self):
        fastk, fastd = STOCHRSI(self.data, self.timeperiod, 5, 3, 0)
        self.stochrsi_data[str(self.timeperiod) + 'Min FASTK'] = fastk
        self.stochrsi_data[str(self.timeperiod) + 'Min FASTD'] = fastd
        return self.stochrsi_data
        
        
class UltOSC(object):

    """
    UltOSC: THE ULTIMATE OSCILLATOR!
    The Ultimate Oscillator is the weighted sum of three oscillators of different time periods.
    The typical time periods are 7, 14 and 28. The values of the Ultimate Oscillator range from zero to 100.
    Values over 70 indicate overbought conditions, and values under 30 indicate oversold conditions.
    Also look for agreement/divergence with the price to confirm a trend or signal the end of a trend.
    """

    def __init__(self, data, timeperiod):
        super(UltOSC, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.ultosc_data = pd.DataFrame()
        
    def calculate(self):
        timeperiod2 = self.timeperiod * 2
        timeperiod3 = timeperiod2 * 2
        ultosc = ULTOSC(self.data, self.timeperiod, timeperiod2, timeperiod3)
        self.ultosc_data[str(self.timeperiod) + 'Min ULTOSC'] = ultosc
        return self.ultosc_data
        

class Willr(object):

    """
    Willr: Williams percent R momentum indicator
    The Williams %R is similar to an unsmoothed Stochastic %K.
    The values range from zero to 100, and are charted on an inverted scale,
    that is, with zero at the top and 100 at the bottom. Values below 20 indicate an
    overbought condition and a sell signal is generated when it crosses the 20 line.
    Values over 80 indicate an oversold condition and a buy signal is generated when it crosses the 80 line.
    Source: http://www.fmlabs.com/reference/default.htm?url=WilliamsR.htm
    """

    def __init__(self, data, timeperiod):
        super(Willr, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.willr_data = pd.DataFrame()
        
    def calculate(self):
        willr = WILLR(self.data, self.timeperiod)
        self.willr_data[str(self.timeperiod) + 'Min WILLR'] = willr
        return self.willr_data


class Atr(object):

    """
    ATR: Average True Range
    The ATR is a Welles Wilder style moving average of the True Range.
    The ATR is a measure of volatility. High ATR values indicate high volatility,
    and low values indicate low volatility, often seen when the price is flat.
    Source: http://www.fmlabs.com/reference/default.htm?url=ATR.htm
    """

    def __init__(self, data, timeperiod):
        super(Atr, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.atr_data = pd.DataFrame()
        
    def calculate(self):
        atr = ATR(self.data, self.timeperiod)
        self.atr_data[str(self.timeperiod) + 'Min ATR'] = atr
        return self.atr_data
        

class Trange(object):

    """
    Trange: True Range
    It is a base calculation that is used to determine the normal trading range of a stock or commodity.
    The greatest of the following: |high[0] - low[0]| , |high[0]-close[-1]| , |low[0] - close[-1]|
    Source: http://www.fmlabs.com/reference/default.htm?url=TR.htm
    """

    def __init__(self, data):
        super(Trange, self).__init__()
        self.data = data
        self.trange_data = pd.DataFrame()
        
    def calculate(self):
        self.trange_data['TRANGE'] = TRANGE(self.data)
        return self.trange_data
        

class Tsf(object):

    """
    TSF: Time Series Forecast
    The Time Series Forecast is determined by calculating a linear regression
    trendline using the "least squares fit" method. The least squares fit technique fits a trendline
    to the data in the chart by minimizing the distance between the data points and the
    linear regression trendline. The interpretation of a Time Series Forecast is identical
    to a moving average. Since the indicator is "fitting" itself to the data rather than averaging them,
    the Time Series Forecast is more responsive to price changes.
    Source: http://www.metastock.com/Customer/Resources/TAAZ/Default.aspx?p=109
    """

    def __init__(self, data, timeperiod):
        super(Tsf, self).__init__()
        self.data = data
        self.timeperiod = timeperiod
        self.tsf_data = pd.DataFrame()
        
    def calculate(self):
        tsf = TSF(self.data, self.timeperiod)
        self.tsf_data[str(self.timeperiod) + 'Min TSF'] = tsf
        return self.tsf_data
        

class Ad(object):

    """
    The Accumulation/Distribution Line is interpreted by looking for a divergence in the direction of the
    indicator relative to price. If the Accumulation/Distribution Line is trending upward it indicates
    that the price may follow. Also, if the Accumulation/Distribution Line becomes flat while the price is still
    rising (or falling) then it signals an impending flattening of the price.
    CLV = ((close-low)-(high-close))/(high-low)
    AD = AD[-1] + CLV*volume
    """

    def __init__(self, data):
        super(Ad, self).__init__()
        self.data = data
        self.ad_data = pd.DataFrame()
        
    def calculate(self):
        self.ad_data['Chaikin A/D Line'] = AD(self.data)
        return self.ad_data
        

class Adosc(object):

    """
    ADOSC: Accumulation Distribution Oscillator
    The Chaikin Oscillator is created by subtracting a 10-period exponential moving average of the
    Accumulation/Distribution Line from a 3-period exponential moving average of the
    Accumulation/Distribution Line.
    Source: http://www.metastock.com/Customer/Resources/TAAZ/Default.aspx?p=41
    """

    def __init__(self, data, timeperiod):
        self.data = data
        self.timeperiod = timeperiod
        self.adosc_data = pd.DataFrame()
        
    def calculate(self):
        fastperiod = self.timeperiod
        slowperiod = fastperiod * 3
        adosc = ADOSC(self.data, fastperiod, slowperiod)
        self.adosc_data[str(self.timeperiod) + 'Min ADOSC'] = adosc
        return self.adosc_data
        