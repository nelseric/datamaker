from datamaker.indicator import *
from datamaker.result import *

from datamaker.feature import Feature
import json
import types
import pandas as pd

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

  def parse_feature(self, feature_data):
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
    features = map(lambda x: x.result(), self.features)
    features_concat = pd.concat(features, axis=1)
    return features_concat
