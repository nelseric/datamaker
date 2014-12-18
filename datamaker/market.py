"""Market context for a strategy"""

class Market(object):
  """Contains market context for a strategy"""
  def __init__(self, arg):
    super(Market, self).__init__()
    self.arg = arg

  def order_history(self, timeframe=None):
    """ Returns a list of previous orders on this account """

  def orders(self):
    """ returns a list of current orders for this market"""
    pass

  def risk(self):
    """ Returns a summary of current orders and risk utilization """
    pass

  def account_size(self):
    """ Returns money in account available for use """
    pass

  def leverage(self):
    """ Returns accounts available leverage """



class Order(object):
  """docstring for Order"""
  def __init__(self):
    super(Order, self).__init__()
    

