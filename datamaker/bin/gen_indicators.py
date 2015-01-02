""" Generating indicators """

from pathlib import Path
import json

import datamaker.db as db


def gen_indicators(path=Path(".")):
    """
        Load the list of indicator sets, get the features and calculate them
        for training data
    """

    # Load sets
    feature_sets = []
    for indicator_file in path.glob("features/*.json"):
        feature_set = json.load(indicator_file.open())
        feature_sets.append(db.FeatureSet.load(feature_set))

    # load project info
    project = json.load((path / "project.json").open())
    for strategy in project["strategies"]:
        db.Strategy.load(strategy)
        # db.DataSet.load(strategy["data_sets"])

    session = db.Session()
    for data_set in session.query(db.DataSet).all():
        data_set.generate(path)
    session.commit()

if __name__ == "__main__":
    gen_indicators()
