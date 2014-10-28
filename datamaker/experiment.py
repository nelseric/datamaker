"""
@author: Eric Nelson
"""
from __future__ import print_function

# pylint: disable=wildcard-import,unused-wildcard-import,star-args,R0902

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

    self.training_set_file = kwargs.get('training_set_file')
    self.validation_set_file = kwargs.get('validation_set_file')

    self.prediction_file = kwargs.get('prediction_file')
    self.model_name = kwargs.get('model_name')
    self.prediction_name = kwargs.get('prediction_name')

    self.instrument = kwargs.get('instrument')
    self.required_data_range = kwargs.get('required_data_range')
    self.limit_upper = kwargs.get('limit_upper')
    self.limit_lower = kwargs.get('limit_lower')
    self.stop_mode = kwargs.get('stop_mode')

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
      print("Calculating {}".format(feature.__class__.__name__))
      feature_data.append(feature.calculate(data))
      
      #necessary to change index of ta_lib indicators to timestamps
      feature_data[0].index = data.index
      
    return pd.concat(feature_data, axis=1)


def parse_feature(feature_data):
  """
    Instantiate and configure a feature class based
    on the experiment definition
  """
  klass = feature_data["class"].split('.')

  cur = globals()[klass.pop(0)]
  while isinstance(cur, types.ModuleType):
    cur = getattr(cur, klass.pop(0))

  params = feature_data.get("parameters", {})
  return cur(**params)
