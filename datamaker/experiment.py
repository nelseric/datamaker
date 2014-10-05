"""
@author: Eric Nelson
"""
from __future__ import print_function

# pylint: disable=wildcard-import,unused-wildcard-import,star-args

from datamaker.indicator import *
from datamaker.result import *

import types
import pandas as pd

class Experiment(object):
  """
    Experiment class, will parse experiment data, and generate configured
    features and classes
  """

  def __init__(self, **kwargs):
    super(Experiment, self).__init__()
    self.name = kwargs.get('name')
    self.description = kwargs.get('description')

    self.database_table = kwargs.get('database_table')
    self.database = pd.HDFStore(kwargs.get('database_file'))

    self.training_set_file = pd.HDFStore(kwargs.get('training_set_file'))
    self.validation_set_file = pd.HDFStore(kwargs.get('validation_set_file'))

    self.instrument = kwargs.get('instrument')

    self.features = [parse_feature(f) for f in kwargs.get("features", [])]
    self.classes = [parse_feature(c) for c in kwargs.get("classes", [])]

  def input_training_data(self):
    """
      Get the data used to generate training data for this experiment
    """
    return self.database.get(self.database_table)

  def calculate(self, data):
    """
      Generate the experiment dataset corresponding with the dataframe provided
    """
    feature_data = []
    for feature in self.features + self.classes:
      print("Calculating {}".format(feature))
      feature_data.append(feature.calculate(data))

    return pd.concat(feature_data, axis=1)


def parse_feature(feature_data):
  """
    Instantiate and configure a feature class based
    on the experiment definition
  """
  print("Loading " + feature_data["class"])
  klass = feature_data["class"].split('.')

  cur = globals()[klass.pop(0)]
  while isinstance(cur, types.ModuleType):
    cur = getattr(cur, klass.pop(0))

  params = feature_data.get("parameters", {})
  return cur(**params)
