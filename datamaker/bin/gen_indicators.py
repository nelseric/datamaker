""" Generating indicators """

import pandas as pd
import numpy as np

from pathlib import Path
import json

import IPython

import datamaker.db as db
import sqlalchemy.exc

def gen_indicators(path=Path(".")):
    """ 
        Load the list of indicator sets, get the features and calculate them
        for training data
    """

    # Load sets
    feature_sets = []
    for indicator_file in path.glob("indicators/*.json"):
        feature_set = json.load(indicator_file.open())
        feature_sets.append(db.FeatureSet.load(feature_set))


    # load project info
    project = json.load((path / "project.json").open())
    for strategy in project["strategies"]:
        indicators = db.DataSet.load(strategy["indicators"])
        session = db.Session()
        IPython.embed()


if __name__ == "__main__":
    gen_indicators()
