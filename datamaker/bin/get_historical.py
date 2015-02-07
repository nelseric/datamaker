""" Main Datamaker Entrypoint"""
from __future__ import print_function
import argparse
from pathlib import Path

import datamaker.db as db


def get_historical():
    """ Get historical"""
    parser = argparse.ArgumentParser(
        description="Datamaker CLI Tool",
        usage='''dm-hist [args]'''
    )
    # parser.add_argument("project_path", default=".", help="Project Directory")
    parser.add_argument(
        "range", type=float, help="Range (in years) of data to get")

    args = parser.parse_args()
    path = Path(".")

    pairs = db.CurrencyPair.load(path)

    for pair in pairs:
        pair.download_historical_data(path, args.range)
        print(len(pair.get_historical_database(path).ohlcv))
        pair.deduplicate_historical(path)
        print(len(pair.get_historical_database(path).ohlcv))

if __name__ == "__main__":
    get_historical()
