""" Run a backtest """
from pathlib import Path

import datamaker.db as db

from datamaker.backtest import Market, Backtest

import IPython


def run_backtest(path=Path(".")):

    session = db.Session()
    strategy = session.query(db.Strategy).first()
    historical = strategy.currency_pair.historical_data(path)

    market = Market(
        historical, instrument="EUR_USD", account_size=100000, leverage=1)

    backtest = Backtest(historical, strategy=strategy, market=market)

    backtest.run()
    IPython.embed()


if __name__ == "__main__":
    run_backtest()
