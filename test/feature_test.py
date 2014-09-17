import pytest
from datamaker.feature import Feature

def test_abstract_indicator():
  ind = Feature("foo")
  assert ind.data == "foo"

  """ This is an abstract class, so these methods should rais an error """
def test_calculate():
  ind = Feature("foo")

  with pytest.raises(NotImplementedError):
    ind.calculate()

def test_result():
  ind = Feature("foo")

  with pytest.raises(NotImplementedError):
    ind.result()
