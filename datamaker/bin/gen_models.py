""" Generating Models """
import numpy as np
import pandas as pd
from pathlib import Path
import json

import datamaker.db as db
import datamaker.model as mlmod
import datamaker.ext.water as water




def gen_models(path=Path(".")):
    """ 
        Train the models and then save them for later
    """

    session = db.Session()

    for strategy in session.query(db.Strategy).all():
        import IPython
        IPython.embed()
        # Initialize model
        model_inst = getattr(mlmod, strategy['model_name'])()

        strategy_name = strategy.name

        model_inst.train(strategy)


            


if __name__ == "__main__":
    gen_models()
