
class Indicator(object):
  """
    Abstract interface for indicator implementation
  """

  def __init__(self, data):
    self.data = data

  def calculate(self):
    raise NotImplementedError("This method must be overwritten.")

  def result(self):
    raise NotImplementedError("This method must be overwritten.")
