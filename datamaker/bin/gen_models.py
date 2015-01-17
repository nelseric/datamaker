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
            model_inst = getattr(mlmod, model_params['model_type'])()

            # Train model on data
            n_samples = 300
            x_data, y_data = make_classification(
                n_samples=n_samples, n_features=4)
            
            import IPython
            IPython.embed()

            data_arg = np.hstack((x_data, np.reshape(y_data, [n_samples, 1])))

            data_arg_train = pd.DataFrame(data_arg[:200, :])
            data_arg_test = pd.DataFrame(data_arg[200:, :])

            model_inst.train(
                data_arg_train, model_params, strat_element)

            # plot performance on test set
            model_inst.visualize(data_arg_test)

            # determine the optimal threshold
            opt_thresh = model_inst.get_threshold(
                data_arg_test)


if __name__ == "__main__":
    gen_models()
