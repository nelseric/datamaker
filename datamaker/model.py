"""
  ML Model Training and prediction
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import os

from pathlib import Path

import datamaker.ext.water as water


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
        return "{}_{}.pkl".format(strategy_params['name'], self.__class__.__name__)

    def save_model(self, strategy_params, path=Path('.')):
        """Saves the Model"""

        pass


class RFModel(Model):

    """
    The Random Forest Model
    """

    def __init__(self):
        super(RFModel, self).__init__()

    def train(self, strategy, path):
        """
        Trains the h2o model performing all necessary steps in h2o
        """

        water_obj = water.API()

        train_file = path.absolute() / \
            (strategy.get_heuristic_path(path).split('.')[0] + '_train.csv.gz')

        val_file = path.absolute() / \
            (strategy.get_heuristic_path(path).split('.')[0] + '_val.csv.gz')

        train_out = water_obj.import_and_parse(str(train_file))

        val_out = water_obj.import_and_parse(str(val_file))

        source = train_out['destination_key']
        response = strategy.heuristic_class.split('.')[-1]
        validation = val_out['destination_key']
        strategy_name = strategy.name

        rf_out = water_obj.rf_train(
            source, response, validation, strategy_name, str(path.absolute()) + '/' + strategy.get_model_path(path) + '/' + strategy.name)

    def predict(self, strategy, path, file_name=''):
        water_obj = water.API()

        if file_name == '':
            file_name = str(path.absolute()) + '/' + \
                strategy.get_heuristic_path(
                    path).split('.')[0] + '_test.csv.gz'

        model_path = str(path.absolute()) + '/' + \
            strategy.get_model_path(path) + '/' + strategy.name

        # Load the prediction file
        pred_import_out = water_obj.import_and_parse(str(file_name))

        # load the model
        load_model_out = water_obj.load_model(model_path)

        import IPython
        IPython.embed()

        pred_out = water_obj.predict(
            load_model_out['model']['_key'], load_model_out['model']['_dataKey'], strategy.name)

        export_out = water_obj.export_files(strategy.name, str(
            path.absolute()) + '/' + strategy.get_model_path(path) + '/' + strategy.name + '.csv')

        #
