# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 13:36:52 2014

@author: alex

"""

# pylint: disable=R0903,C0111,C0301

import talib.abstract as ta
import pandas as pd
from datamaker.feature import Feature


class TALibIndicator(Feature):

  """
  Super Class for Indicator implementation that sets the data to the proper
  "ohlcv" dictionary format used by ta-lib and accepts a timeperiod.
  """

  def __init__(self, timeperiod, *args, **kwargs):
    super(TALibIndicator, self).__init__(*args, **kwargs)
    self.timeperiod = timeperiod
    
  def calculate(self, data):
    #Is data from Oanda or Dukascopy? 
    if 'volume' in data.columns.get_values():
      talib_data = {'open':  data['Ask_open'],
                    'high':  data['Ask_high'],
                    'low':   data['Ask_low'],
                    'close': data['Ask_close'],
                    'volume':data['volume']}
    elif 'Ask_volume' and 'Bid_volume' in data.columns.get_values():
      talib_data = {'open':  data['Ask_open'],
                    'high':  data['Ask_high'],
                    'low':   data['Ask_low'],
                    'close': data['Ask_close'],
                    'volume':data['Bid_volume']+data['Ask_volume']}
    return super(TALibIndicator, self).calculate(talib_data)


class Adx(TALibIndicator):

  """
  Average Directional Movement Index (ADX) is an indicator of trend strength
  in a series of prices.
  ADX is a lagging indicator and will rang between 0-100
  ADX < 20 indicates trend weakness
  ADX > 40 indicates trend strength
  ADX > 50 indicates an extremely strong trend
  """
  
  def _calculate(self, data):
    adx_data = pd.DataFrame()
    adx = ta.ADX(data, self.timeperiod)
    adx_data[str(self.timeperiod) + 'Min ADX'] = adx
    return adx_data

class Adxr(TALibIndicator):

  """
  The Average Directional Movement Index Rating (ADXR) measures the strength of the ADX
  ADXR(i) = (ADX(i) + ADX(i-n))/2 where n = ADXR interval
  ADXR ranges from 0-100
  lower values reflect weak trend
  higher values reflect strong trend
  Helps better display trends in volatile markets
  """
  
  def _calculate(self, data):
    adxr_data = pd.DataFrame()
    adxr = ta.ADXR(data, self.timeperiod)
    adxr_data[str(self.timeperiod) + 'Min ADXR'] = adxr
    return adxr_data

class Aroon(TALibIndicator):

  """
  The Aroon indicator is used to identify trends and likelihood that trends will reverse
  Made up of two lines:
    -Aroonup: measures strength of an upward trend
    -Aroondown: measures strength of a downward trend
  Each line reports a percentage of total time it takes for the price to reach the highest and lowest
  points over a given time period and ranges from 0-100%, 0 being weak trend, and 100 being strong trend
  """
  
  def _calculate(self, data):
    aroon_data = pd.DataFrame()
    aroondown, aroonup = ta.AROON(data, self.timeperiod)
    aroon_data[str(self.timeperiod) + 'Min Aroondown'] = aroondown
    aroon_data[str(self.timeperiod) + 'Min Aroonup'] = aroonup
    return aroon_data

class Aroonosc(TALibIndicator):

  """
  The Aroon Oscillator(AROONOSC uses Aroonup and Aroondown to gauge the strength of a current trend
  and the likelihood that it will continue.
  AROONOSC = Aroonup - Aroondown
  AROONOSC > 0 indicates uptrend is present
  AROONOSC < 0 indicates a downtrend is present
  """
  
  def _calculate(self, data):
    aroonosc_data = pd.DataFrame()
    aroonosc = ta.AROONOSC(data, self.timeperiod)
    aroonosc_data[str(self.timeperiod) + 'Min AROONOSC'] = aroonosc
    return aroonosc_data

class Bop(TALibIndicator):

  """
  The Balance of Power (BOP) measures the strength of the bulls vs. the bears by assessing
  the ability of each to push price to extreme levels
  Balance Power = (Close - Open)/(High - Low)
  Balance of Power (BOP) = SMA(Balance Power)
  BOP > 0 indicates buy signal, Increasing BOP indicates upward trend
  BOP < 0 indicates sell signal, Decreasing BOP indicates downward trend
  """
  
  def _calculate(self, data):
    bop_data = pd.DataFrame()
    bop_data['BOP'] = ta.BOP(data)
    return bop_data

class Cci(TALibIndicator):

  """
  The Commodity Channel Inex (CCI) quantifies the relationship between the assets price,
  a moving average(SMA) of the assets price and normal deviations(D) from that average.
  CCI = (PRICE - SMA) / (.015 * D)
  Sell Signal:
    CCI > 100 and started to trend downwards
  Buy Signal:
    CCI < -100 and started to trend upwards
  """

  def _calculate(self, data):
    cci_data = pd.DataFrame()
    cci = ta.CCI(data, self.timeperiod)
    cci_data[str(self.timeperiod) + 'Min CCI'] = cci
    return cci_data

class Cmo(TALibIndicator):

  """
  The Chande Momentum Oscillator (CMO)
  S(u) - Sum of difference between todays close and yesterdays close
  S(d) - Absolute Value of the difference between todays close and yesterdays close
  CMO = ( S(u) - S(d) ) / ( S(u) + S(d) ) * 100
  CMO range (-100,+100)
  CMO > +50 indicates overbought
  CMO < -50 indicates oversold
  """

  def _calculate(self, data):
    cmo_data = pd.DataFrame()
    cmo = ta.CMO(data, self.timeperiod)
    cmo_data[str(self.timeperiod) + 'Min CMO'] = cmo
    return cmo_data

class Macd(TALibIndicator):

  """
  _calculates MACD indicator using common timeperiod intervals.
  """

  def _calculate(self, data):
    macd_data = pd.DataFrame()
    macd, macdsignal, macdhist = ta.MACD(data, 12*self.timeperiod, 26*self.timeperiod, 9*self.timeperiod)
    macd_data[str(self.timeperiod) + 'Min MACD'] = macd
    macd_data[str(self.timeperiod) + 'Min MACD Signal'] = macdsignal
    macd_data[str(self.timeperiod) + 'Min MACD Hist'] = macdhist
    return macd_data

class Mfi(TALibIndicator):

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

  def _calculate(self, data):
    mfi_data = pd.DataFrame()
    mfi = ta.MFI(data, self.timeperiod)
    mfi_data[str(self.timeperiod) + 'Min MFI'] = mfi
    return mfi_data

class Minus_DI(TALibIndicator):

  """
  The Negative Directional Indicator is used to measure the presence of a downtrend
  MINUS_DI sloping upward indicates the strength of downtrend is increasing
  """

  def _calculate(self, data):
    minusdi_data = pd.DataFrame()
    minusdi = ta.MINUS_DI(data, self.timeperiod)
    minusdi_data[str(self.timeperiod) + 'Min MINUS_DI'] = minusdi
    return minusdi_data

class Mom(TALibIndicator):

  """
  The Momentum Indicator is used to measure the velocity of price change
  MOM = Current_Close Price - N-Period Ago Close Price
  Values will produce line indicating whether prices are rising or falling over N-period
  """

  def _calculate(self, data):
    mom_data = pd.DataFrame()
    mom = ta.MOM(data, self.timeperiod)
    mom_data[str(self.timeperiod) + 'Min MOM'] = mom
    return mom_data

class Ppo(TALibIndicator):

  """
  Percentage Price Oscillator (PPO) shows relationship among two moving averages
  Result is a percentage revealing where short term average is relative to long term average
  A PPO of 10 means the short term average is 10% above the long term average
  """

  def _calculate(self, data):
    ppo_data = pd.DataFrame()
    ppo = ta.PPO(data, 9*self.timeperiod, 26*self.timeperiod, 1)
    ppo_data[str(self.timeperiod) + 'Min PPO'] = ppo
    return ppo_data

class Roc(TALibIndicator):

  """
  Rate of Change:
  A technical indicator that measures the percentage change between the most recent price and the
  price "n" periods in the past.
  It is _calculated by using the following formula:
  (Closing Price Today - Closing Price "n" Periods Ago) / Closing Price "n" Periods Ago

  ROC is classed as a price momentum indicator or a velocity indicator because
  it measures the rate of change or the strength of momentum of change.
  """

  def _calculate(self, data):
    roc_data = pd.DataFrame()
    roc = ta.ROC(data, self.timeperiod)
    roc_data[str(self.timeperiod) + 'Min ROC'] = roc
    return roc_data

class Rocr(TALibIndicator):

  """
  Rate of Change Ratio indicates the rate of change as a ratio over N-periods
  """

  def _calculate(self, data):
    rocr_data = pd.DataFrame()
    rocr = ta.ROCR(data, self.timeperiod)
    rocr_data[str(self.timeperiod) + 'Min ROCR'] = rocr
    return rocr_data

class Rsi(TALibIndicator):

  """
  Relative Strength Index (RSI) compares the magnitude of recent gains to recent losses
  to determine overbought and oversold conditions.
  RSI = 100 - 100/(1 + RS)
  RS = Average of N period up closes / Average of N periods down closes
  RSI ranges from 0-100
  RSI >= 70 indicates overbought
  RSI <= 30 indicates oversold
  """

  def _calculate(self, data):
    rsi_data = pd.DataFrame()
    rsi = ta.RSI(data, self.timeperiod)
    rsi_data[str(self.timeperiod) + 'Min RSI'] = rsi
    return rsi_data

class Stoch(TALibIndicator):

  """
  Stochastic Oscillator compares closing price to a price range over an N-period of time
  In an upward trending market prices tend to close near their high
  In a downward trending market prices tend to close near their low
  A transaction signal occurs when slowk and slowd cross
  """

  def _calculate(self, data):
    stoch_data = pd.DataFrame()
    slowk, slowd = ta.STOCH(data, self.timeperiod, 3*1440, 0*1440, 3*1440, 0*1440)
    stoch_data[str(self.timeperiod) + 'Min SLOWK'] = slowk
    stoch_data[str(self.timeperiod) + 'Min SLOWD'] = slowd
    return stoch_data

class StochF(TALibIndicator):

  """
  Stochastic Oscillator Fast is similar to Stochastic Oscillator but is more
  sensitive to changing prices.
  Transaction signal occurs when fastk and fastd cross
  """
  
  def _calculate(self, data):
    stochf_data = pd.DataFrame()
    fastk, fastd = ta.STOCHF(data, self.timeperiod, 3*1440, 0*1440)
    stochf_data[str(self.timeperiod) + 'Min FASTK'] = fastk
    stochf_data[str(self.timeperiod) + 'Min FASTD'] = fastd
    return stochf_data

class StochRSI(TALibIndicator):

  """
  Stochastic Relative Strength Index takes the Stochastic Oscillator of RSI values
  Ranges between 0 and 1
  STOCHRSI < 0.20 indicates oversold
  STOCHRSI > 0.80 indicates overbought
  """

  def _calculate(self, data):
    stochrsi_data = pd.DataFrame()
    fastk, fastd = ta.STOCHRSI(data, self.timeperiod, 5*1440, 3*1440, 0*1440)
    stochrsi_data[str(self.timeperiod) + 'Min FASTK'] = fastk
    stochrsi_data[str(self.timeperiod) + 'Min FASTD'] = fastd
    return stochrsi_data

class UltOSC(TALibIndicator):

  """
  UltOSC: THE ULTIMATE OSCILLATOR!
  The Ultimate Oscillator is the weighted sum of three oscillators of different time periods.
  The typical time periods are 7, 14 and 28. The values of the Ultimate Oscillator range from zero to 100.
  Values over 70 indicate overbought conditions, and values under 30 indicate oversold conditions.
  Also look for agreement/divergence with the price to confirm a trend or signal the end of a trend.
  """

  def _calculate(self, data):
    ultosc_data = pd.DataFrame()
    timeperiod2 = self.timeperiod * 2
    timeperiod3 = timeperiod2 * 2
    ultosc = ta.ULTOSC(data, self.timeperiod, timeperiod2, timeperiod3)
    ultosc_data[str(self.timeperiod) + 'Min ULTOSC'] = ultosc
    return ultosc_data

class Willr(TALibIndicator):

  """
  Willr: Williams percent R momentum indicator
  The Williams %R is similar to an unsmoothed Stochastic %K.
  The values range from zero to 100, and are charted on an inverted scale,
  that is, with zero at the top and 100 at the bottom. Values below 20 indicate an
  overbought condition and a sell signal is generated when it crosses the 20 line.
  Values over 80 indicate an oversold condition and a buy signal is generated when it crosses the 80 line.
  Source: http://www.fmlabs.com/reference/default.htm?url=WilliamsR.htm
  """

  def _calculate(self, data):
    willr_data = pd.DataFrame()
    willr = ta.WILLR(data, self.timeperiod)
    willr_data[str(self.timeperiod) + 'Min WILLR'] = willr
    return willr_data

class Atr(TALibIndicator):

  """
  ATR: Average True Range
  The ATR is a Welles Wilder style moving average of the True Range.
  The ATR is a measure of volatility. High ATR values indicate high volatility,
  and low values indicate low volatility, often seen when the price is flat.
  Source: http://www.fmlabs.com/reference/default.htm?url=ATR.htm
  """

  def _calculate(self, data):
    atr_data = pd.DataFrame()
    atr = ta.ATR(data, self.timeperiod)
    atr_data[str(self.timeperiod) + 'Min ATR'] = atr
    return atr_data

class Trange(TALibIndicator):

  """
  Trange: True Range
  It is a base calculation that is used to determine the normal trading range of a stock or commodity.
  The greatest of the following: |high[0] - low[0]| , |high[0]-close[-1]| , |low[0] - close[-1]|
  Source: http://www.fmlabs.com/reference/default.htm?url=TR.htm
  """

  def _calculate(self, data):
    trange_data = pd.DataFrame()
    trange_data['TRANGE'] = ta.TRANGE(data)
    return trange_data

class Tsf(TALibIndicator):

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

  def _calculate(self, data):
    tsf_data = pd.DataFrame()
    tsf = ta.TSF(data, self.timeperiod)
    tsf_data[str(self.timeperiod) + 'Min TSF'] = tsf
    return tsf_data

class Ad(TALibIndicator):

  """
  The Accumulation/Distribution Line is interpreted by looking for a divergence in the direction of the
  indicator relative to price. If the Accumulation/Distribution Line is trending upward it indicates
  that the price may follow. Also, if the Accumulation/Distribution Line becomes flat while the price is still
  rising (or falling) then it signals an impending flattening of the price.
  CLV = ((close-low)-(high-close))/(high-low)
  AD = AD[-1] + CLV*volume
  """

  def _calculate(self, data):
    ad_data = pd.DataFrame()
    ad_data['Chaikin A/D Line'] = ta.AD(data)
    return ad_data

class Adosc(TALibIndicator):

  """
  ADOSC: Accumulation Distribution Oscillator
  The Chaikin Oscillator is created by subtracting a 10-period exponential moving average of the
  Accumulation/Distribution Line from a 3-period exponential moving average of the
  Accumulation/Distribution Line.
  Source: http://www.metastock.com/Customer/Resources/TAAZ/Default.aspx?p=41
  """

  def _calculate(self, data):
    adosc_data = pd.DataFrame()
    fastperiod = self.timeperiod
    slowperiod = fastperiod * 3
    adosc = ta.ADOSC(data, fastperiod, slowperiod)
    adosc_data[str(self.timeperiod) + 'Min ADOSC'] = adosc
    return adosc_data
