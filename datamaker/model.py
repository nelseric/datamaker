"""
  ML Model Training and prediction
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import os

from pathlib import Path


class Model(object):

    """
    Parent class for all machine learning classfiers and regressors
    """

    def __init__(self):
        super(Model, self).__init__()
        self.ml_mod = []

    
    def load_model(self, strategy_params, path=''):
        """Loads the model from a pickled file"""
        pass
        

    def get_prediction(self, data):
        "Get prediction from features, used in real-time prediction"
        pass


    def get_threshold(self, data):
        """
        Finds the optimal threshold. 
        opt_thesh = arg_max{thresh}{((1+SBF)^(.5+SBF)(1-SBF)^(.5-SBF))^(days_attempted)
        to make this not such a large number we will optimize the log(opt_thresh)
        this is just fine because the log(opt_thresh) monotonically increases
        with opt_thresh
        where SBF is the supplemental boosting factor
        """
        pass

    def model_name(self, strategy_params):
        return "{}_{}.pkl".format(strategy_params['name'], self.__class__.__name__ )

    def save_model(self, strategy_params, path=Path('.')):
        """Saves the Model"""

        pass


class RFModel(Model):

    """
    The Random Forest Model
    """

    def __init__(self):
        super(ETCModel, self).__init__()

    def train(self, data, y_name, model_params, strategy_params):
        """
        
        """

        pass
