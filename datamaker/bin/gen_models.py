""" Generating Models """

from pathlib import Path
import json

import datamaker.db as db
from datamaker.model import Model


def gen_models(path=Path(".")):
    """ 
        Train the models and then save them for later
    """

    # Load data
    model_sets = []
    for model_file in path.glob("models/*.json"):
        model_params = json.load(model_file.open())
        import IPython
        IPython.embed()

    # Initialize model

    # Train model on data

    # Save model


if __name__ == "__main__":
    gen_models()
