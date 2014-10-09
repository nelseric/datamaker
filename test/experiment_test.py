"""
@author = Eric Nelson
"""

import pytest
import pandas as pd
import json

from datamaker.experiment import Experiment

def test_module_import():
  assert Experiment

def test_experiment_parse():
  experiment = Experiment(**json.load(open("test/fixtures/experiment.json")))

  ds = pd.HDFStore("test/fixtures/GBPUSD.h5")

  data = ds.get("ticks_ohlcv")

  assert experiment.calculate(pd.DataFrame(data)).__class__ == pd.DataFrame
