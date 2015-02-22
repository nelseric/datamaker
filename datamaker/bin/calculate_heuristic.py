""" Entrypoint for calculating heuristics """

from __future__ import print_function

from pathlib import Path

import datamaker.db as db
from multiprocessing import Pool


def calculate(strategy_id, path):
    session = db.Session()
    strategy = session.query(db.Strategy).get(strategy_id)

    print("{}:{} Starting".format(strategy.currency_pair.instrument,
                                  strategy.heuristic()))
    strategy.calculate_heuristic(path)
    print("{}:{} Complete".format(strategy.currency_pair.instrument,
                                  strategy.heuristic()))


def calculate_heuristic(path=Path(".")):
    """ Calculate and store all the heuristics"""

    session = db.Session()

    pool = Pool()
    results = []

    for strategy in session.query(db.Strategy).all():
        results.append(
            pool.apply_async(func=calculate, args=(strategy.id, path)))
    pool.close()
    pool.join()

if __name__ == "__main__":
    calculate_heuristic()
