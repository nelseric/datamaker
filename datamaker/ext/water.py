""" Wrapper for H2O's REST Interface """

from __future__ import print_function
import json
import requests


class EndpointsMixin(object):

    """ Administration Methods """

    def get_jobs(self, **params):
        """ Get the list of running H2O jobs """

        endpoint = "Jobs.json"
        return self.request(endpoint, params=params)

    def cluster_status(self, **params):
        """ Get the cluster status """

        endpoint = "Cloud.json"
        return self.request(endpoint, params=params)

    def network_test(self, **params):
        """ Get the cluster speed """

        endpoint = "2/NetworkTest.json"
        return self.request(endpoint, params=params)

    def shutdown(self, **params):
        """ Shut down the cluster """

        endpoint = "Shutdown.json"
        return self.request(endpoint, params=params)


class API(EndpointsMixin, object):

    """
    H2O API Client
    :param api_url: 
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


class WaterError(Exception):

    """ Generic error class, catches oanda response errors
    """

    def __init__(self, error_response):
        msg = "H2O API returned error code %s (%s) " % (
            error_response['code'], error_response['message'])

        super(WaterError, self).__init__(msg)
