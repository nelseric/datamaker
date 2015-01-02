""" Join datasets into training data """

from pathlib import Path
import json

import datamaker.db as db


def join_datasets(path=Path(".")):
    """
        Load the list of indicator sets, get the features and calculate them
        for training data
    """

    session = db.Session()
    for data_set in session.query(db.DataSet).all():
        data_set.join(path)
    session.commit()

if __name__ == "__main__":
    join_datasets()
