import pytest
import pandas.util.testing as tm
from datamaker.indicator.ewma import NormalizedEWMA
import pandas as pd

def test_normalized_ewma():
  d = pd.HDFStore("test/fixtures/GBPUSD.h5").get("ticks_ohlcv")

  ewma =  NormalizedEWMA(span = 4)
  assert ewma.span == 4
  assert ewma.calculate(d).__class__ == pd.DataFrame
