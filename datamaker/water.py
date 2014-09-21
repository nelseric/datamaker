class Water(object):
  """docstring for Water"""
  def __init__(self, h2o_url):
    super(Water, self).__init__()
    self.h2o_url = h2o_url

  def upload_training_data(self, training_dataframe):
    pass

  def get_prediction(self, realtime_dataframe):
    prediction_id = self._upload_realtime_data(realtime_dataframe)

    self._generate_prediction(prediction_id)

    prediction_data = self._download_prediction(prediction_id)

    self._cleanup_prediction(prediction_id)

    return prediction_data
    

  def _upload_realtime_data(self, realtime_dataframe):
    return "1"

  def _generate_prediction(prediction_id):
    """ Will block until prediction is calculated? """
    return true

  def _download_prediction(prediction_id):
    return true # Buy some shit

  def _cleanup_prediction(prediction_id):
    return true
