"""
@author: Eric Nelson
"""
from __future__ import print_function

import time
import os

from datamaker.brokers.oanda_broker import OandaBroker
from datamaker.water import Water

import datetime, pytz

class MarketManager(object):
  """
    Gets prices, Sends them to H2O, and then buys stuff
    depending on the result H2O Gives
  """
  def __init__(self, experiment, *args, **kwargs):
    super(MarketManager, self).__init__(*args, **kwargs)

    self.experiment = experiment

    oanda_acct = kwargs.get("oanda_acct", os.environ.get("OANDA_ACCOUNT", ""))
    oanda_token = kwargs.get("oanda_token", os.environ.get("OANDA_TOKEN", ""))
    oanda_env = kwargs.get("oanda_env", os.environ.get("OANDA_ENV", ""))

    self.oanda = OandaBroker(oanda_acct, oanda_token, oanda_env)
    self.water = Water(self.experiment.prediction_file,
                       self.experiment.model_name,
                       self.experiment.prediction_name)
    time_dif = datetime.timedelta(seconds=experiment.required_data_range)
    self.start_time = datetime.datetime.now(tz=pytz.utc) - time_dif

  def run(self, interval=30.0):
    """
      Run the manager, checking for new data or orders every [interval]
    """
    while self.check():
      time.sleep(interval)

  def check(self):
    """
    Get new data from the broker, send it to H2O to make a prediction,
    and place an order
    """

    raw_data = self.oanda.gather_data(instrument_arg=self.experiment.instrument,
                                      start_time=self.start_time.isoformat())
    raw_data.drop(['complete', 'time'], axis=1, inplace=True)

    data = self.experiment.calculate(raw_data)
    current = data.ix[len(data)-1:len(data)-0]
    prediction = self.water.get_prediction(current)

    print(current.index[-1])
    if prediction > (1E-3):
      if (self.oanda.get_num_trades() < 4):
        print("Buy")
        self._place_order(current, prediction)
      else:
        print("Can't buy, too many orders")
    print(prediction)
    return True

  def _place_order(self, current, confidence):
    """
      Place an order whee we are confident
    """
    price = self.oanda.get_cur_bid(self.experiment.instrument)
    upper = price + self.experiment.limit_upper
    lower = price - self.experiment.limit_lower
    
    if (self.experiment.stop_mode == 'ts'):
      self.oanda.place_order_ts(self.experiment.instrument,
                             lower, upper, int(10000))
    else:
      self.oanda.place_order(self.experiment.instrument,
                             lower, upper, int(10000))


