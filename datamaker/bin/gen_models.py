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

    strategy_params = json.load((path / 'project.json').open())

    for strat_element in strategy_params['strategies']:
        for model_file in path.glob("models/*.json"):
            # Load data
            model_params = json.load(model_file.open())

            # Initialize model
            model_inst = getattr(mlmod, model_params['model_type'])(path)

            # Train model on data
            x_data, y_data = make_classification(n_samples=300, n_features=4)

            model_inst.train(
                x_data[:200, :], y_data[:200], model_params, strat_element)

            # plot performance on test set
            model_inst.visualize(x_data[200:, :], y_data[200:])

            # determine the optimal threshold
            opt_thresh = model_inst.get_threshold(
                x_data[200:, :], y_data[200:])


if __name__ == "__main__":
    gen_models()
