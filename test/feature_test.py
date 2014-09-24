import pytest
from datamaker.feature import Feature

import types

def test_abstract_indicator():
  feature = Feature(data = "foo")
  assert feature.data == "foo"

  """ This is an abstract class, so these methods should rais an error """
def test_calculate():
  feature = Feature(data = "foo")

  with pytest.raises(NotImplementedError):
    feature.calculate()

def test_result_when_calculate_is_not_defined():
  feature = Feature(data = "foo")
  with pytest.raises(NotImplementedError):
    feature.result()

def test_result_when_calculate_is_defined():
  feature = Feature(data = "foo")

  def calculator(self):
    self._result = "Foo Bar"

  # methods are not automatically bound to object instances, so we have to do it ourselves
  # See http://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object
  feature.calculate = types.MethodType(calculator, feature)
  assert feature.result() == "Foo Bar"
