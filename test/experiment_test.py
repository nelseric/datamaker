import pytest
from datamaker.experiment import Experiment

def test_module_import():
  assert Experiment
  assert Experiment().things()

def test_experiment_parse():
  experiment = Experiment.load_file("fixtures/experiment.json")
