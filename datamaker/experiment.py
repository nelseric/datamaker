from datamaker.indicator import *

class Experiment(object):
  """Experiment class, will parse experiment data, and generate stuff"""
  def __init__(self):
    super(Experiment, self).__init__()
    ewma.NormalizedEWMA

  @staticmethod
  def load_file(experiment_file):
    pass

  def things(self):
    return [ewma.NormalizedEWMA, macd.MACD]
