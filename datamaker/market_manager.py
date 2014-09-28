import argparse
import json
import time

from datamaker.experiment import Experiment

def run():
  parser = argparse.ArgumentParser(description='Run an experiment')
  parser.add_argument('experiment', type=argparse.FileType('r'),
    help='Experiment parameter JSON file'
    )

  args = parser.parse_args()
  manager = MarketManager(Experiment(json.load(args.experiment)))
  while(manager.check()):
    time.sleep(1.0)

class MarketManager(object):
  """
    Gets prices, Sends them to H2O, and then buys stuff depending on the result H2O Gives
  """
  def __init__(self, experiment):
    super(MarketManager, self).__init__()
    self.experiment = experiment

  def check(self):
    print("Foo")
    return False
