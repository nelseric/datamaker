import pytest
from datamaker.experiment import Experiment

def test_module_import():
  assert Experiment

def test_experiment_parse():
  experiment = Experiment.load(open("test/fixtures/experiment.json"))