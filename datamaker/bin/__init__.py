""" Main Datamaker Entrypoint"""
from __future__ import print_function
import argparse
from pathlib import Path

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

if __name__ == "__main__":
    dm_main()
