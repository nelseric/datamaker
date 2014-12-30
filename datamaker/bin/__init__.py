""" Main Datamaker Entrypoint"""
from __future__ import print_function
import argparse
from pathlib import Path

import datamaker.db as db


def dm_main():
    """ Main DM Entrypoint"""
    parser = argparse.ArgumentParser(
        description="Datamaker CLI Tool",
        usage='''dm [args]'''
    )
    # parser.add_argument("project_path", default=".", help="Project Directory")
    parser.add_argument(
        "range", type=float, help="Range (in years) of data to get")

    args = parser.parse_args()
    path = Path(".")

    db.Base.metadata.create_all(db.engine)

    pairs = db.CurrencyPair.load(path)

    for pair in pairs:
        pair.download_historical_data(path, args.range)

if __name__ == "__main__":
    dm_main()
