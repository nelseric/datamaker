""" Generating Models """
import numpy as np
import pandas as pd
from pathlib import Path
import json

import datamaker.db as db
import datamaker.model as mlmod

from sklearn.datasets import make_classification


def gen_models(path=Path(".")):
    """ 
        Train the models and then save them for later
    """

    session = db.Session()

    for strategy in session.query(db.Strategy).all():
        for model_file in path.glob("models/*.json"):
            # Load data
            model_params = json.load(model_file.open())

            # Initialize model
            model_inst = getattr(mlmod, model_params['model_type'])()

            s_name = strategy.name

            data_tot = strategy.load_features(path).copy()
            h_tot = strategy.load_heuristic(path).copy()
            data_tot =pd.concat((data_tot, h_tot), axis = 1, copy = False)

            train_bound = np.floor(
                model_params['training_size'] * len(data_tot))
            val_bound = train_bound + np.floor(
                model_params['validation_size'] * len(data_tot))
            test_bound = val_bound + np.floor(
                model_params['test_size'] * len(data_tot))

            data_train = data_tot.iloc[:train_bound, :].copy()
            data_valid = data_tot.iloc[train_bound:val_bound, :].copy()
            data_test = data_tot.iloc[val_bound:test_bound, :].copy()

            model_inst.train(
                data_train, model_params, s_name)

            model_inst.visualize(data_valid)
            opt_thresh = model_inst.get_threshold(
                data_valid)

            


if __name__ == "__main__":
    gen_models()
