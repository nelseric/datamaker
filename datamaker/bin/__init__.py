""" Main Datamaker Entrypoint"""
from __future__ import print_function
import argparse
from pathlib import Path
import json

import datamaker.db as db
import datamaker.db.base


def dm_main():
    """ Main DM Entrypoint"""
    parser = argparse.ArgumentParser(
        description="Datamaker CLI Tool",
        usage='''dm [args]'''
    )

    path = Path(".")

    data_path = path / "data"
    if not data_path.exists():
        data_path.mkdir()

    db.base.Base.metadata.create_all(db.engine)

    db.CurrencyPair.load(path)    # Load sets

    feature_sets = []
    for indicator_file in path.glob("features/*.json"):
        feature_set = json.load(indicator_file.open())
        feature_sets.append(db.FeatureSet.load(feature_set))

    # load project info
    project = json.load((path / "project.json").open())
    for strategy in project["strategies"]:
        db.Strategy.load(strategy)

if __name__ == "__main__":
    dm_main()
