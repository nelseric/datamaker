""" Generating Models """
import numpy as np
import pandas as pd
from pathlib import Path
import json

import datamaker.db as db
import datamaker.model as mlmod


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
            model_inst = getattr(mlmod,model_params['model_type'])(path)

            # Train model on data
            feature_data = np.zeros([100,5])
            model_inst.train(model_params, feature_data, strat_element)


        




if __name__ == "__main__":
    gen_models()
