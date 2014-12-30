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
        """Saves the model as a pickled file"""

    def load_model(self):
        """Loads the model from a pickled file"""

    def _preprocess(self, feature_data):
        """
        Makes the data ready for classification
        see: http://scikit-learn.org/0.11/modules/preprocessing.html
        """

        




class ETCModel(Model):

    """
    The Extremely Random Forest Classifier (ExtraTreesClassifier)
    """
    def __init__(self):
        super(ETCModel, self).__init__()

    def train(self, model_params, feature_data):
        """
        Trains the ETC Model
        """

        #Instantiate the models
        mod_inst = ExtraTreesClassifier()
        mod_inst.set_params(**model_params['all_params']['model_params'])
        meta_est = BaggingClassifier(mod_inst)
        meta_est.set_params(**model_params['all_params']['bagging_params'])

        #Preprocess the data
        _preprocess(feature_data)




