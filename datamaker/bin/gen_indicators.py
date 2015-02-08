""" Generating indicators """

from pathlib import Path

import datamaker.db as db


def gen_indicators(path=Path(".")):
    """
        Load the list of indicator sets, get the features and calculate them
        for training data
    """

    session = db.Session()
    for strategy in session.query(db.Strategy).all():
        strategy.calculate_training_data(path)
    session.commit()

if __name__ == "__main__":
    gen_indicators()
