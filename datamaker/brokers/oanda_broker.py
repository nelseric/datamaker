import ext.oandapy as oandapy
from datamaker.broker import Broker
import numpy as np
import pandas as pd

class OandaBroker(Broker):
  """
    OANDA Broker implementing our own broker interface
    This needs to be provided with config csv that holds
    the environment and the
  """
  def __init__(self, account_id, access_token, trading_env):
    super(OandaBroker, self).__init__()
    self.account_id = account_id
    self.access_token = access_token
    self.trading_env = trading_env

    self.oanda = oandapy.API(environment=self.trading_env, access_token=self.access_token)


  def get_cur_allocation(self):
    """
    Returns the total amount currently invested in all currency pairs
    """
    response = self.oanda.get_positions(self.account_id)
    all_positions = response.get('positions')
    allocations = [all_positions[x]['units'] for x in range(0, len(all_positions))]

    return sum(allocations)

  def place_order(self, *args, **kwargs):
    """
    Requests an order to be placed on a currency pair
    """
    instrument_arg = kwargs.get('instrument', 'EUR_USD')
    units_arg = kwargs.get('units', '1')
    side_arg = kwargs.get('side', 'buy')
    type_arg = kwargs.get('type', 'limit')
    take_profit = kwargs.get('takeProfit', 2)
    stop_loss = kwargs.get('stopLoss', 1)

    response = self.oanda.create_order(self.account_id, instrument=instrument_arg,
                                     units=units_arg, side=side_arg,
                                     type=type_arg, takeProfit = take_profit,
                                     stopLoss = stop_loss)
    return True

  def close_orders(self):
    """
    Closes all open orders on the broker
    """

  def gather_data(self, *args, **kwargs):
    """
    Downloads all data from start_time until current moment
    """
    instrument_arg = kwargs.get('instrument', 'EUR_USD')
    granularity_arg = kwargs.get('granularity', 'M1')
    candle_format = kwargs.get('candleFormat', 'bidask')
    start_time = kwargs.get('start', '2014-09-01T00:00:00.000000Z')
    count_arg = kwargs.get('count',5000)
    out_data = []
    data_complete = False
    while(data_complete != True):
      response = self.oanda.get_history(instrument = instrument_arg,
                                        granularity = granularity_arg,
                                        candleFormat = candle_format,
                                        start = start_time,
                                        count = count_arg)
      raw_data = response['candles']
      if (len(out_data) == 0):
        out_data = out_data + raw_data
      elif (len(out_data) >1):
        #raw_data[0] is already in out_data as raw_data[-1] from last iteration
        out_data = out_data + raw_data[1:]
      start_time = raw_data[-1]['time']
      if (len(raw_data) < 5000):
        data_complete = True
    
    out_data = self._list_to_df(out_data)
    return out_data

  def update_data(self, data):
    """
    Updates self.data with current ohlcv data from broker
    """
    start_time = data.index[-1].strftime("%Y-%m-%dT%H:%M:%S.000000Z")
    temp_data = self.gather_data(start = start_time)
    temp_data = self._list_to_df(temp_data)
    if (len(temp_data) > 1):
      #temp_data[0] is the same as data[-1]
      out_data = data.append(temp_data[1:])
    return out_data
    
  def _list_to_df(self, data):
    """
    Converts list of dictionaries to dataframe
    """
    indices = pd.tseries.index.DatetimeIndex([data[x]['time'] for x in range(0,len(data))])
    outData = pd.DataFrame(data,index = indices)
    outData.columns = ['Ask_close', 'Bid_close', 'complete',
                       'Ask_high', 'Bid_high', 'Ask_low', 
                       'Bid_low', 'Ask_open', 'Bid_open',
                       'time', 'volume']
    return outData

    
