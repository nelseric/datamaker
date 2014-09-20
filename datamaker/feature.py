class Feature(object):
  """
    Abstract interface for NN feature implementation
  """

  def __init__(self, data):
    self.data = data
    self._result = None

  def calculate(self):
    raise NotImplementedError("The method calculate method must be overwritten and set self._result")

  def result(self):
    if self._result == None:
      self.calculate()
      if self._result == None:
        raise NotImplementedError("The method calculate method must set self._result")

    return self._result
