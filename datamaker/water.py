import numpy as np
import pandas as pd
import urllib

class Water(object):
  """
  This class controls interaction with H2O. Note that in order for many
  of these methods to work H2O must be instantiated and contain requisite 
  data objects such as pre-trained neural networks
  """
  def __init__(self, data_path, *args, **kwargs):
    super(Water, self).__init__()
    self.h2o_url = kwargs.get('h2o_url', 'http://localhost:54321/')
    self.data_path = data_path
    self.rt_file_name = kwargs.get('rt_file_name', 'rt_file_name')
    self.model_name = kwargs.get('model_name', 'test1')
    self.pred_name = kwargs.get('pred_name', 'rt_pred')
    
    

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
    realtime_dataframe.to_csv(self.data_path+self.rt_file_name + '.csv')
    import_url = '2/ImportFiles2.json?'
    params = { 'path' : self.data_path + self.rt_file_name + '.csv'}
    tot_url = self.h2o_url + import_url + urllib.urlencode(params)

    self._send_url(tot_url)

    self._parse_data()
    
    return True

  def _parse_data(self):
    """
    Converts raw uploaded data to processed H2o data set
    """
    parse_url = '2/Parse2.json?'
    params = {'parser_type' : 'AUTO',
              'separator' : '-1',
              'header' : '1',
              'single_quotes' : '0',
              'header_from_file' : '',
              'exclude' : '',
              'source_key' : 'nfs:/' + self.data_path + self.rt_file_name + '.csv',
              'preview' : '0'
              }
    tot_url = self.h2o_url + parse_url + urllib.urlencode(params)
    
    self._send_url(tot_url)
  
    return True
              
    

  def _generate_prediction(self):
    """
    Runs pre-trained model on uploaded data in h2o
    """
    predict_url = '2/Predict.json?'
    
    params = {'model' : self.model_name,
              'data' : self.rt_file_name + '.hex',
              'prediction' : self.pred_name + '.hex'
              }
    tot_url = self.h2o_url + predict_url + urllib.urlencode(params)
    
    self._send_url(tot_url)
    
    return True

  def _download_prediction(self):
    """
    Downloads prediction reads the confidence level for buy action
    """
    pred_export_url = '2/ExportFiles.json?'
    params = {'src_key' : self.pred_name + '.hex',
              'path' : self.data_path + self.pred_name + '.csv',
              'force' : '1'
              }
    tot_url = self.h2o_url + pred_export_url + urllib.urlencode(params)
    
    self._send_url(tot_url)
    
    pred_df = pd.read_csv(self.data_path + self.pred_name + '.csv')   
    confidence = pred_df['setosa'][0]
    
    return confidence 
    
  

  def _cleanup_prediction(self):
    """
    Removes input data from h2o
    """
    clean_url = 'Remove.json?'
    params = {'key' : self.rt_file_name + '.hex' }
    tot_url = self.h2o_url + clean_url + urllib.urlencode(params)
    
    self._send_url(tot_url)
    
    params = {'key' : self.pred_name + '.hex' }
    tot_url = self.h2o_url + clean_url + urllib.urlencode(params)
    
    self._send_url(tot_url)
    
    return True
    
  def _send_url(self,tot_url):
    """
    Repeatedly sends commands to h2o until command 
    is processed properly
    """
    while(1):
      try:
        url_out = urllib.urlopen(tot_url).read()
        print url_out
        if (url_out.split('"')[1] != 'error'):
          raise('request completed succesfully')
      except:
        break
      