""" Entrypoint for calculating heuristics """

from __future__ import print_function

from pathlib import Path

import datamaker.db as db


def calculate_heuristic(path=Path(".")):
    """ Calculate and store all the heuristics"""

    session = db.Session()

    for strategy in  session.query(db.Strategy).all():
        print("{}:{}".format(strategy.currency_pair.instrument, strategy.heuristic()))
        strategy.calculate_heuristic(path)

if __name__ == "__main__":
    calculate_heuristic()
