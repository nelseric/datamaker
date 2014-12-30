""" Generating Models """

from pathlib import Path
import json

import datamaker.db as db
import datamaker.model as mlmod


def gen_models(path=Path(".")):
    """ 
        Train the models and then save them for later
    """

    
    model_sets = []
    for model_file in path.glob("models/*.json"):
        # Load data
        model_params = json.load(model_file.open())

        # Initialize model
        model_inst = getattr(mlmod,model_params['model_type'])()

        # Train model on data
        model_inst.train(model_params)

        # Save model

        import IPython
        IPython.embed()




if __name__ == "__main__":
    gen_models()
