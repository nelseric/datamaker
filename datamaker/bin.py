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
  parser.add_argument("range", type=float, help="Range (in years) of data to get")

  args = parser.parse_args()
  path = Path(".")

  db.Base.metadata.create_all(db.engine)

  pairs = db.CurrencyPair.load(path)

  dbpath = path / 'data' / "pairs"

  if not dbpath.exists():
    dbpath.mkdir()

  for pair in pairs:

    pair.get_historical(dbpath, args.range)

import pandas as pd

from datamaker.backtest import Market, Backtest
from datamaker.strategy.naive import NaiveBuy



def run_backtest(path=Path(".")):
  historical = pd.HDFStore(str(path / "data" / "pairs" / "EUR_USD.h5")).get("ohlcv")

  market = Market(historical, instrument="EUR_USD", account_size=100000, leverage=1)

  strategy = NaiveBuy(market=market, take_profit=100, stop_loss=100)

  bt = Backtest(historical, strategy=strategy, market=market)

  bt.run()

  IPython.embed()
