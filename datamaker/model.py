"""
  ML Model Training and prediction
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import preprocessing
from sklearn.externals import joblib
from sklearn.metrics import roc_curve
from sklearn.metrics import precision_recall_curve

import matplotlib.pyplot as plt
import os


class Model(object):

    """
    Parent class for all machine learning classfiers and regressors
    """

    def __init__(self, path):
        super(Model, self).__init__()
        self.path = path
        self.ml_mod = []

    def load_model(self, model_name):
        """Loads the model from a pickled file"""

    def visualize(self, test_data_x, test_data_y):
        """
        Plots the ROC curve of the ml model
        """
        test_data_y_pred = self.ml_mod.predict_proba(test_data_x)

        fpr, tpr, _ = roc_curve(test_data_y[:], test_data_y_pred[:, 1])

        precision, recall, _ = precision_recall_curve(
            test_data_y[:], test_data_y_pred[:, 1])

        plt.figure()
        plt.plot(fpr, tpr)
        plt.show()
        import IPython
        IPython.embed()

    def _preprocess(self, x_data, y_data):
        """
        Makes the data ready for classification; specifically this will 
        normalize the data and 
        see: http://scikit-learn.org/stable/modules/preprocessing.html
        """

        # Scale the data first (zero mean, unit variance)
        x_data = preprocessing.scale(x_data)

        # Remove rows with NaN values within
        keep_ind = ~np.isnan(x_data).any(axis=1)
        x_data = x_data[keep_ind]
        y_data = y_data[keep_ind]

        return x_data, y_data


class ETCModel(Model):

    """
    The Extremely Random Forest Classifier (ExtraTreesClassifier)
    """

    def __init__(self, path):
        super(ETCModel, self).__init__(path)

    def train(self, x_data, y_data, model_params, strategy_params):
        """
        Trains the ETC Model
        """

        # Instantiate the models
        mod_inst = ExtraTreesClassifier()
        mod_inst.set_params(**model_params['all_params']['model_params'])
        meta_est = BaggingClassifier(mod_inst)
        meta_est.set_params(**model_params['all_params']['bagging_params'])

        # Preprocess the data
        x_data, y_data = self._preprocess(x_data, y_data)

        # Train the model
        meta_est.fit(x_data, y_data)
        self.ml_mod = meta_est

        # Save the model
        self.save_model(strategy_params)

    def save_model(self, strategy_params):
        """Saves the model as a pickled file"""

        pkl_path = 'models/' + strategy_params['instrument'] + '_ETC/'
        if (not(os.path.isdir(pkl_path))):
            os.mkdir(pkl_path)
        joblib.dump(self.ml_mod, pkl_path + 'model.pkl')
