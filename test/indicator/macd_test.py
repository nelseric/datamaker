import pytest
import pandas.util.testing as tm
from datamaker.indicator.macd import MACD
import pandas as pd

def test_macd():
  d = pd.DataFrame([2,2,2,2] * 10000)
  macd =  MACD(data = d)
  tm.assert_frame_equal(macd.data, d)
