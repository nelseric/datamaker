class OandaBroker(object):
  """
    OANDA Broker implementing our own broker interface
  """
  def __init__(self, arg):
    super(OandaBroker, self).__init__()
    
  def get_cur_allocation(self):
    """
    Returns the total amount currently invested in all currency pairs
    """
  
  def place_order(self):
    """
    Requests an order to be placed on a currency pair
    """
    
  def close_orders(self):
    """
    Closes all open orders on the broker
    """
    
  def gather_data(self, start_time):
    """
    Downloads all data from start_time until current moment
    """
    #Call _query_broker_hist, iterate until complete
    
  def update_data(self):
    """
    Updates self.data with current ohlcv data from broker
    """
  
  def _query_broker_hist(self, start_time):
    """
    Downloads 5000 data points from broker, helper method for
    update_data and gather_data
    """