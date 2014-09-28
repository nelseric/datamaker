from datamaker.feature import Feature

class Feature(Feature):
  """Sets result to be data"""
  def __init__(self, *args, **kwargs):
    super(Feature, self).__init__(*args, **kwargs)

  def calculate(self):
    self._result = self.data
