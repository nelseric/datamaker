import numpy as np
import pandas as pd
import urllib
from bs4 import BeautifulSoup

class Water(object):
  """
  This class controls interaction with H2O. Note that in order for many
  of these methods to work H2O must be instantiated and contain requisite 
  data objects such as pre-trained neural networks
  """
  def __init__(self,data_path):
    super(Water, self).__init__()
    self.h2o_url = 'http://localhost:54321/'
    self.data_path = data_path
    self.rt_file_name = 'rt_file_name.csv'
    self.model_name = 'nn2'
    self.pred_name = 'rt_pred'
    

  def upload_training_data(self, training_dataframe):
      """
      Will be used for automation of training
      """
      
      
      return "1"

  def get_prediction(self, realtime_dataframe):
    """
    
    """
    self._upload_realtime_data(realtime_dataframe)

    self._generate_prediction()

    prediction_data = self._download_prediction()

    self._cleanup_prediction(prediction_id)

    return True
    

  def _upload_realtime_data(self, realtime_dataframe):
    """
    Uploads real-time data from broker for real-time prediction
    """
    #Save dataframe first
    realtime_dataframe.to_csv(self.data_path+self.rt_file_name)
    import_url = '2/ImportFiles2.json?'
    params = { 'path' : self.data_path + self.rt_file_name}
    tot_url = self.h2o_url + import_url + urllib.urlencode(params)
    print tot_url
    urllib.urlopen(tot_url)
    
    self._parse_data()
    return "1"

  def _parse_data(self):
    """
    
    """
    parse_url = '2/Parse2.json?'
    params = {'parser_type' : 'AUTO',
              'separator' : '-1',
              'header' : '1',
              'single_quotes' : '0',
              'header_from_file' : '',
              'exclude' : '',
              'source_key' : 'nfs:/' + self.data_path + self.rt_file_name,
              'preview' : '0'
              }
    tot_url = self.h2o_url + parse_url + urllib.urlencode(params)
    print tot_url
    url_out = urllib.urlopen(tot_url)
#    if (url_out.find('error') ==2):
#        assert('Bad URL')        
#        return 0
    
    return 1
              
    

  def _generate_prediction(self):
    """
    Runs pre-trained model on uploaded data in h2o
    """
    predict_url = '2/Predict.json?'
    h2o_file_name = self.rt_file_name.split('.')[0]
    params = {'model' : self.model_name,
              'data' : h2o_file_name + '.hex',
              'prediction' : self.pred_name + '.hex'
              }
    tot_url = self.h2o_url + predict_url + urllib.urlencode(params)
    url_out = urllib.urlopen(tot_url)
    
    print tot_url 
    
    return True

  def _download_prediction(self):
    """
    
    """
    pred_export_url = '2/ExportFiles.json?'
    params = {'src_key' : self.pred_name + '.hex',
              'path' : self.data_path + self.pred_name + '.csv',
              'force' : '1'
              }
    tot_url = self.h2o_url + pred_export_url + urllib.urlencode(params)
    urllib.urlopen(tot_url)
    print tot_url
    pred_df = pd.read_csv(self.data_path + self.pred_name + '.csv')   
    confidence = pred_df['1'][0]
    
    return True # Buy some shit
    
  

  def _cleanup_prediction(prediction_id):
     
    return True

if __name__=='__main__':
    aaa = Water('/home/nater/Documents/')
    bbb = pd.read_csv('/home/nater/Downloads/iris.csv')
    aaa.get_prediction(bbb)
   
