from datamaker.indicator import *
from datamaker.result import *

from datamaker.feature import Feature
import json
import types
import pandas as pd

class Experiment(object):
  """Experiment class, will parse experiment data, and generate stuff"""

  @staticmethod
  def load(experiment_json):
    expmt = json.load(experiment_json)
    return Experiment(**expmt)

  def __init__(self, *args, **kwargs):
    super(Experiment, self).__init__()
    self.name = kwargs.get('name')
    self.description = kwargs.get('description')
    self.tick_file = kwargs.get('tick_file')
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
    return pd.DataFrame([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
