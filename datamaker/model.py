"""
  ML Model Training and prediction
"""


class Model(object):

    """
        Parent class for all machine learning classfiers and regressors
    """

    def __init__(self, strategy):
        super(Model, self).__init__()
        self.strategy = strategy

    def save_model(self):
        "Saves the model as a pickled file"

    def load_model(self):
        "Loads the model from a pickled file"


class ETCModel(Model):

    """
        The Extremely Random Forest Classifier (ExtraTreesClassifier)
    """

    def train(self, model_params):
        "Trains the ETC Model"
