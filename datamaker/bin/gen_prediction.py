""" Generating Predictions """
import numpy as np
import pandas as pd
from pathlib import Path
import json

import datamaker.db as db
import datamaker.model as mlmod
import datamaker.ext.water as water


def gen_prediction(path=Path("."), file_name=''):
    """ 
        generate prediction for a given file

        Takes in optional parameter file; which is what 
        the model will try to predict on; otherwise the 
        model will predict on the the test set file.
    """

    session = db.Session()

    for strategy in session.query(db.Strategy).all():
        # Initialize model
        model_inst = getattr(mlmod, strategy.model_class.split('.')[-1])()

        model_inst.predict(strategy, path)



if __name__ == "__main__":
    gen_prediction()
