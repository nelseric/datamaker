"""
  ML Model Training and prediction
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import preprocessing
from sklearn.externals import joblib
import os


class Model(object):

    """
    Parent class for all machine learning classfiers and regressors
    """

    def __init__(self, path):
        super(Model, self).__init__()
        self.path = path

    def load_model(self, model_name):
        """Loads the model from a pickled file"""

    def _preprocess(self, feature_data):
        """
        Makes the data ready for classification; specifically this will 
        normalize the data and 
        see: http://scikit-learn.org/stable/modules/preprocessing.html
        """

        # Scale the data first (zero mean, unit variance)
        feature_data = preprocessing.scale(feature_data)

        # Remove rows with NaN values within
        feature_data = feature_data[~np.isnan(feature_data).any(axis=1)]

        return feature_data


class ETCModel(Model):

    """
    The Extremely Random Forest Classifier (ExtraTreesClassifier)
    """

    def __init__(self, path):
        super(ETCModel, self).__init__(path)

    def train(self, model_params, feature_data, strategy_params):
        """
        Trains the ETC Model
        """

        # Instantiate the models
        mod_inst = ExtraTreesClassifier()
        mod_inst.set_params(**model_params['all_params']['model_params'])
        meta_est = BaggingClassifier(mod_inst)
        meta_est.set_params(**model_params['all_params']['bagging_params'])

        # Preprocess the data
        feature_data = self._preprocess(feature_data)

        # Train the model
        meta_est.fit(feature_data[:, 0:-2], feature_data[:, -1])

        # Save the model
        self.save_model(meta_est, strategy_params)

    def save_model(self, ml_mod, strategy_params):
        """Saves the model as a pickled file"""
        
        pkl_path = 'models/' + strategy_params['instrument'] + '_ETC/'
        os.mkdir(pkl_path)
        joblib.dump(ml_mod, pkl_path + 'model.pkl')
