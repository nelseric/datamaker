"""
@author: Nathan Ward, Eric Nelson
"""

# pylint: disable=C0301

import pandas as pd
import urllib
import requests

import os.path

from StringIO import StringIO

class Water(object):
  """
  This class controls interaction with H2O. Note that in order for many
  of these methods to work H2O must be instantiated and contain requisite 
  data objects such as pre-trained neural networks
  """
  def __init__(self, prediction_input_path, model_name, prediction_key,
               h2o_url='http://localhost:54321/'):
    super(Water, self).__init__()

    self.h2o_url = h2o_url
    self.prediction_input_path = os.path.join(os.path.abspath('.'), prediction_input_path)
    self.prediction_input_key = os.path.basename(prediction_input_path).replace('csv', 'hex')
    self.model_name = model_name
    self.prediction_key = prediction_key
    
    

  def upload_training_data(self, training_dataframe):
    """
    Will be used for automation of training
    """
    pass
    

  def get_prediction(self, realtime_dataframe):
    """
    Uploads dataframe, generates prediction, reads prediction, 
    removes uploaded data
    """
    
    self._upload_realtime_data(realtime_dataframe)
    self._generate_prediction()
    prediction_data = self._download_prediction()
    self._cleanup_prediction()

    return prediction_data
    

  def _upload_realtime_data(self, realtime_dataframe):
    """
    Uploads real-time data from broker for real-time prediction
    """
    #Save dataframe first
    realtime_dataframe.to_csv(self.prediction_input_path, index=False)
    import_url = '2/ImportFiles2.json?'
    params = {'path': self.prediction_input_path}

    response = requests.get(self.h2o_url + import_url, params=params)
    while response.status_code != 200:
      print response.status_code
      response = requests.get(self.h2o_url + import_url, params=params)

    self._parse_data()
    
    return True

  def _parse_data(self):
    """
    Converts raw uploaded data to processed H2o data set
    """
    parse_url = '2/Parse2.json?'
    params = {'parser_type' : 'CSV',
              'separator' : '-1',
              'header' : '1',
              'single_quotes' : '0',
              'header_from_file' : '',
              'exclude' : '',
              'source_key' : 'nfs:/' + self.prediction_input_path,
              'preview' : '0'}

    tot_url = self.h2o_url + parse_url + urllib.urlencode(params)
    
    self._send_url(tot_url)
  
    return True
              
    

  def _generate_prediction(self):
    """
    Runs pre-trained model on uploaded data in h2o
    """
    predict_url = '2/Predict.json?'
    
    params = {'model' : self.model_name,
              'data' : self.prediction_input_key,
              'prediction' : self.prediction_key}

    tot_url = self.h2o_url + predict_url + urllib.urlencode(params)
    
    self._send_url(tot_url)
    
    return True

  def _download_prediction(self):
    """
    Downloads prediction reads the confidence level for buy action
    """
    pred_export_url = '2/DownloadDataset.json?'
    params = {'src_key' : self.prediction_key}
    
    response = requests.get(self.h2o_url + pred_export_url, params=params)
    while response.status_code != 200:
      print response.status_code
      response = requests.get(self.h2o_url + pred_export_url, params=params)
      
    res_io = StringIO(response.text)
    pred_df = pd.read_csv(res_io)

    return pred_df['1'][0]
  

  def _cleanup_prediction(self):
    """
    Removes input data from h2o
    """
    clean_url = 'Remove.json?'
    params = {'key': self.prediction_input_key}
    tot_url = self.h2o_url + clean_url + urllib.urlencode(params)

    self._send_url(tot_url)
    
    params = {'key': self.prediction_key}
    tot_url = self.h2o_url + clean_url + urllib.urlencode(params)
    
    self._send_url(tot_url)
    
    return True
    
  def _send_url(self, tot_url):
    """
    Repeatedly sends commands to h2o until command 
    is processed properly
    """
    while True:
      try:
        url_out = urllib.urlopen(tot_url).read()
        # print url_out
        if (url_out.split('"')[1] != 'error'):
          raise('request completed succesfully')
      except:
        break
      