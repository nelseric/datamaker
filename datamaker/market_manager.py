import argparse
import json
import time

import dotenv
import os

from datamaker.experiment import Experiment

import datamaker.brokers.oanda_broker import OandaBroker

import IPython


def run():
  dotenv.load_dotenv('.env')

  parser = argparse.ArgumentParser(description='Run an experiment')
  parser.add_argument('experiment', type=argparse.FileType('r'),
    help='Experiment parameter JSON file'
    )

  args = parser.parse_args()

  manager = MarketManager(Experiment.load(args.experiment))

  while(manager.check()):
    time.sleep(1.0)

  IPython.embed()


class MarketManager(object):
  """
    Gets prices, Sends them to H2O, and then buys stuff depending on the result H2O Gives
  """
  def __init__(self, experiment, *args, **kwargs):
    super(MarketManager, self).__init__(*args, **kwargs)

    self.experiment = experiment

    oanda_acct = kwargs.get("oanda_acct", os.environ.get("OANDA_ACCT", ""))
    oanda_token = kwargs.get("oanda_token", os.environ.get("OANDA_TOKEN", ""))
    oanda_env = kwargs.get("oanda_env", os.environ.get("OANDA_ENV", ""))

    self.oanda = OandaBroker(oanda_acct, oanda_token, oanda_env)



  def check(self):
    print(self.oanda)
    return False
