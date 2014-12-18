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
  args = parser.parse_args()
  path = Path(".")

  db.Base.metadata.create_all(db.engine)

  pairs = db.CurrencyPair.load(path)

  dbpath = path / 'data' / "pairs"

  if not dbpath.exists():
    dbpath.mkdir()

  for pair in pairs:

    pair.get_historical(dbpath, 0.25)
