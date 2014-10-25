"""
@author: Eric Nelson
"""
from __future__ import print_function

import argparse

import dotenv
import json

from datamaker.experiment import Experiment

from datamaker.market_manager import MarketManager


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
