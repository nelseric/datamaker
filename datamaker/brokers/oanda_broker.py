#import ext.oandapy as oab
import sys
import ConfigParser

import ext.oandapy as oandapy

class OandaBroker(object):
  """
    OANDA Broker implementing our own broker interface
    This needs to be provided with config csv that holds 
    the environment and the 
  """
  def __init__(self):
    super(OandaBroker, self).__init__()
    #################### change this section later ############################
    self.env_name = 'practice'
    self.token_name = 'xxx'
    self.account_id = 9999999
    ###########################################################################
    self.oanda = oandapy.API(environment=self.env_name, access_token=self.token_name)
    
    
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
    
    return out_data
    
  def update_data(self, data):
    """
    Updates self.data with current ohlcv data from broker
    """
  