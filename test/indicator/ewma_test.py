import pytest
import pandas.util.testing as tm
from datamaker.indicator.ewma import NormalizedEWMA
import pandas as pd

def test_normalized_ewma():
  d = pd.DataFrame([1,2,3,4])
  ewma =  NormalizedEWMA(data = d, span = 4)
  tm.assert_frame_equal(ewma.data, d)
  assert ewma.span == 4
