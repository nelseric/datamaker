from datamaker.indicator import *
from datamaker.result import *

from datamaker.feature import Feature
import json
import types
import pandas as pd
import numpy as np

import IPython

import re

import argparse
import dotenv
import os
def gen_training_data():
  dotenv.load_dotenv('.env')

  parser = argparse.ArgumentParser(description='Run an experiment')
  parser.add_argument('experiment', type=argparse.FileType('r'),
    help='Experiment parameter JSON file'
    )

  parser.add_argument('training_set_file', type=argparse.FileType('w'),
    help='Output training set CSV for NN'
    )

  parser.add_argument('validation_set_file', type=argparse.FileType('w'),
    help='Output validation set CSV for NN'
    )

  args = parser.parse_args()

  experiment = Experiment.load(args.experiment)
  data = experiment.result()

  data.columns = map(
    lambda col: re.sub("\('(\w+)', '(\w+)'\)","\\1_\\2", col),
    data.columns
  )

  validation_size = int(0.10 * len(data))

  validation_set = np.random.choice(data.index, validation_size, replace=False)
  training_set = np.setdiff1d(data.index.values, validation_set)
  validation_set = data.ix[validation_set]
  training_set = data.ix[training_set]

  training_set.to_csv(args.training_set_file, index=False)
  validation_set.to_csv(args.validation_set_file, index=False)


class Experiment(object):
  """Experiment class, will parse experiment data, and generate configured features and classes"""

  @staticmethod
  def load(experiment_json):
    expmt = json.load(experiment_json)
    return Experiment(**expmt)

  def __init__(self, *args, **kwargs):
    super(Experiment, self).__init__()
    self.name = kwargs.get('name')
    self.description = kwargs.get('description')

    self.database_file = kwargs.get('database_file')
    self.database_table = kwargs.get('database_table')
    self.database = pd.HDFStore(self.database_file)

    self.instrument = kwargs.get('instrument')

    self.features = map(self.parse_feature, kwargs.get("features", []))
    self.classes = map(self.parse_feature, kwargs.get("classes", []))
    self._result = None

  def parse_feature(self, feature_data):
    print("Generating " + feature_data["class"])
    klass = feature_data["class"].split('.')
    cur = globals()[klass.pop(0)]
    while isinstance(cur, types.ModuleType):
      cur = getattr(cur, klass.pop(0))

    params = feature_data.get("parameters", {})
    params["data"] = self.get_input_data()

    return cur(**params)

  def get_input_data(self):
    return self.database.get(self.database_table)

  def calculate(self):
    features = map(lambda x: x.result(), self.features + self.classes)
    self._result = pd.concat(features, axis=1)

  def result(self):
    if self._result is None:
      self.calculate()
      if self._result is None:
        raise NotImplementedError("The method calculate method must set self._result")

    return self._result
