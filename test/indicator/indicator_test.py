import pytest
from datamaker.indicator import indicator as ai

def test_abstract_indicator():
  ind = ai.Indicator("foo")
  assert ind.data == "foo"

  """ This is an abstract class, so these methods should rais an error """
def test_calculate():
  ind = ai.Indicator("foo")

  with pytest.raises(NotImplementedError):
    ind.calculate()

def test_result():
  ind = ai.Indicator("foo")

  with pytest.raises(NotImplementedError):
    ind.result()
