"""
@author: Eric Nelson
"""
import datamaker.feature as s

class Feature(s.Feature):
  """Sets result to be data"""
  def __init__(self, *args, **kwargs):
    super(Feature, self).__init__(*args, **kwargs)

  def calculate(self, data):
    return data
