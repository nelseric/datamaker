class Feature(object):
  """
    Abstract interface for NN feature implementation
  """

  def __init__(self, **kwargs):
    self.shift = kwargs.pop('shift', 0)

  def calculate(self, data):
    """
      The method calculate method must be overwritten and should return 
        a dataframe with 
    """  
    raise NotImplementedError()
