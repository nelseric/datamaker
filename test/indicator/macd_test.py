import pytest
import pandas.util.testing as tm
from datamaker.indicator.macd import MACD
import pandas as pd

def test_macd():
  d = pd.HDFStore("test/fixtures/GBPUSD.h5").get("ticks_ohlcv")
  macd = MACD()
  assert macd.calculate(d).__class__ == pd.DataFrame
