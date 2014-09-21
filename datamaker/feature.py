class Feature(object):
  """
    Abstract interface for NN feature implementation
  """

  def __init__(self, *args, **kwargs):
    self.data = kwargs.pop('data')
    self._result = None

  def calculate(self):
    raise NotImplementedError("The method calculate method must be overwritten and set self._result")

  def result(self):
    if self._result is None:
      self.calculate()
      if self._result is None:
        raise NotImplementedError("The method calculate method must set self._result")

    return self._result
