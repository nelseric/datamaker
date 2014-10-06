"""
@author: Eric Nelson
"""
from __future__ import print_function

import argparse

import time

import dotenv
import os
import json

from datamaker.experiment import Experiment

from datamaker.brokers.oanda_broker import OandaBroker
from datamaker.water import Water

import datetime, pytz

def run():
  """
  Run the market manager and check every second
  """

  dotenv.load_dotenv('.env')

  parser = argparse.ArgumentParser(description='Run an experiment')
  parser.add_argument('experiment', type=argparse.FileType('r'),
                      help='Experiment parameter JSON file')

  args = parser.parse_args()

  experiment = Experiment(**json.load(args.experiment))
  manager = MarketManager(experiment)
  manager.run()


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
    if prediction > 0.6:
      print("Buy")
      self._place_order(current, prediction)
    print(prediction)
    return True

  def _place_order(self, current, confidence):
    """
      Place an order whee we are confident
    """
    price = current["Bid_close"][0]
    upper = price + self.experiment.limit_upper
    lower = price - self.experiment.limit_lower
    self.oanda.place_order(self.experiment.instrument,
                           lower, upper, int(confidence * 10000))


