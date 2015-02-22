""" Main Datamaker Entrypoint"""
from __future__ import print_function
import argparse
from pathlib import Path

import datamaker.db as db

from multiprocessing import Pool

def _get_hist(pair_id, path, range):
    session = db.Session()
    pair = session.query(db.CurrencyPair).get(pair_id)
    return pair.download_historical_data(path, range)


def get_historical(path=Path(".")):
    """ Get historical"""
    parser = argparse.ArgumentParser(
        description="Datamaker CLI Tool",
        usage='''dm-hist [args]'''
    )
    parser.add_argument(
        "range", type=float, help="Range (in years) of data to get")
    args = parser.parse_args()

    session = db.Session()
    pairs = session.query(db.CurrencyPair).all()
    pool = Pool()
    for pair in pairs:
        pool.apply_async(_get_hist, args=(pair.id, path, args.range))
    pool.close()
    pool.join()

    for pair in pairs:
        print(len(pair.get_historical_database(path).ohlcv))
        pair.deduplicate_historical(path)
        print(len(pair.get_historical_database(path).ohlcv))

if __name__ == "__main__":
    get_historical()
