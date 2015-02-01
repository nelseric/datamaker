""" Wrapper for H2O's REST Interface """

from __future__ import print_function
import requests
import time
import datetime


class EndpointsMixin(object):

    """ Administration Methods """

    def network_test(self, **params):
        """ Get the cluster speed """

        endpoint = "2/NetworkTest.json"
        return self.request(endpoint, params=params)

    def shutdown(self, **params):
        """ Shut down the cluster """

        endpoint = "Shutdown.json"
        return self.request(endpoint, params=params)

    def get_jobs(self, **params):
        """ Get the list of running H2O jobs """

        endpoint = "Jobs.json"
        return self.request(endpoint, params=params)

    def cluster_status(self, **params):
        """ Get the cluster status """

        endpoint = "Cloud.json"
        return self.request(endpoint, params=params)

    """ Training and Testing Methods """
    
    def import_files(self, path, **params):
        """
        Uploads data to h2o
        required params:
        path = path of a data file on the hard disk
        """
        endpoint = "2/ImportFiles2.json"
        params['path'] = path

        return self.request(endpoint, params=params)

    def parse(self, source_key, **params):
        """
        Converts raw uploaded data to processed H2o data set
        required params:
        source_key = the name of the imported file in h2o
        eg: nfs://path_name/data_file.csv
        """
        endpoint = '2/Parse2.json'
        params['source_key'] = source_key

        return self.request(endpoint, params=params)

    def DRF(self, source, response, validation, strategy_name, **params):
        """
        Begins to train Big Data Random Forest
        required params:
        source = name of the training file
        response = name of the column being predicted
        validation = name of the validation set
        strategy_name = name of the strategy
        """

        endpoint = '2/DRF.json'

        # timestamp
        ts = time.time()
        # formated timestamp
        fts = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
        default_params = {
            'classification': 1,
            'keep_cross_validation_splits': 0,
            'ntrees': 2000,
            'max_depth': 80,
            'min_rows': 1,
            'nbins': 10000,
            'sample_rate': .05,
            'build_tree_one_node': 0
        }

        params['destination_key'] = 'rf_' + strategy_name + '_' + fts
        params['source'] = source
        params['response'] = response
        params['validation'] = validation

        default_params.update(params)

        return self.request(endpoint, params=default_params)

    def save_model(self, model, path, **params):
        """
        Saves the trained model somewhere on the hard disk
        required params:
        model = name of the model in H2O session
        path = path and filename of the saved file
        """
        endpoint = '2/SaveModel.json'

        default_params = {}
        default_params['force'] = 1
        default_params['save_cv'] = 1

        params['model'] = model
        params['path'] = path

        default_params.update(params)

        return self.request(endpoint, params=default_params)

    def load_model(self, path, **params):
        """
        Loads saved model from the hard disk
        required params:
        path = path and filename of the model on the hard disk
        """
        endpoint = '2/LoadModel.json'

        params['path'] = path

        return self.request(endpoint, params=params)

    def predict(self, model, data, prediction, **params):
        """
        Runs pre-trained model on uploaded data in h2o
        required params:
        model = name of the model in H2O session
        data = name of the data file in H2O session
        """
        endpoint = '2/Predict.json'

        params['model'] = model
        params['data'] = data
        params['prediction'] = prediction

        return self.request(endpoint, params=params)

    def export_files(self, src_key, path, **params):
        """
        Saves the predictions as a csv
        src_key = name of the data in h2o being outputted
        path = path and file name of output file on the hard disk
        """
        endpoint = '2/ExportFiles.json'

        default_params = {}
        default_params['force'] = 1

        params['src_key'] = src_key
        params['path'] = path

        default_params.update(params)

        return self.request(endpoint, params=default_params)

    def remove(self, key, **params):
        """
        Removes input data from h2o
        key = name of the data in h2o session being outputted 
        """
        endpoint = 'Remove.json'

        params['key'] = key

        return self.request(endpoint, params=params)


class API(EndpointsMixin, object):

    """
    H2O API Client
    :param api_url: URL to H2O
    """

    def __init__(self, api_url="http://localhost:54321"):
        super(API, self).__init__()
        self.api_url = api_url
        self.client = requests.Session()

    def request(self, endpoint, method='GET', params=None):
        """Returns dict of response from H2O's open API

        :param endpoint: (required) H2O API endpoint (e.g. 2/ImportData.json)
        :type endpoint: string
        :param method: (optional) Method of accessing data, either GET or POST. (default GET)
        :type method: string
        :param params: (optional) Dict of parameters (if any) accepted the by H2O API endpoint you are trying to access (default None)
        :type params: dict or None
        """

        url = '%s/%s' % (self.api_url, endpoint)

        method = method.lower()
        params = params or {}

        func = getattr(self.client, method)

        request_args = {}
        if method == 'get':
            request_args['params'] = params
        else:
            request_args['data'] = params

        try:
            response = func(url, **request_args)
        except requests.RequestException as error:
            print(str(error))

        # error message
        if response.status_code >= 400:
            raise WaterError(response.content)
            
        if response.json()["error"]:
            raise WaterError(response.json()["error"])

        return response.json()

    def __repr__(self):
        return "water.API({.api_url})".format(self)

class Response(object):
    """H2O Response Object"""

    def __init__(self, data):
        super(Response, self).__init__()
        self.data = data

    def is_redirect(self):
        pass
        


class WaterError(Exception):

    """ Generic error class, catches oanda response errors
    """

    def __init__(self, error_response):
        msg = "H2O API returned error code %s (%s) " % (
            error_response['code'], error_response['message'])

        super(WaterError, self).__init__(msg)
