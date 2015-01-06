""" Run a backtest """
from pathlib import Path

import pandas as pd

from datamaker.backtest import Market, Backtest
from datamaker.strategy.naive import NaiveBuy

import IPython


def run_backtest(path=Path(".")):
    historical = pd.HDFStore(
        str(path / "data" / "pairs" / "EUR_USD.h5")).get("ohlcv")

    market = Market(
        historical, instrument="EUR_USD", account_size=100000, leverage=1)

    strategy = NaiveBuy(market=market, take_profit=100, stop_loss=100)

    backtest = Backtest(historical, strategy=strategy, market=market)

    backtest.run()
    IPython.embed()


if __name__ == "__main__":
    run_backtest()
