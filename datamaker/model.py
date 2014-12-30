"""
  ML Model Training and prediction
"""
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier

class Model(object):

    """
        Parent class for all machine learning classfiers and regressors
    """

    def __init__(self):
        super(Model, self).__init__()
        

    def save_model(self):
        "Saves the model as a pickled file"

    def load_model(self):
        "Loads the model from a pickled file"


class ETCModel(Model):

    """
        The Extremely Random Forest Classifier (ExtraTreesClassifier)
    """
    def __init__(self):
        super(ETCModel, self).__init__()

    def train(self, model_params):
        """
        Trains the ETC Model
        mp: model parameters
        """
        mod_inst = ExtraTreesClassifier()
        mod_inst.set_params(**model_params['all_params']['model_params'])
        meta_est = BaggingClassifier(mod_inst)
        meta_est.set_params(**model_params['all_params']['bagging_params'])

