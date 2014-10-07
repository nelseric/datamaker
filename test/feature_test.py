"""
@author: Eric Nelson
"""
import pytest
from datamaker.feature import Feature

import types

def test_abstract_indicator():
  feature = Feature(shift=3)
  assert feature.shift == 3
  assert feature._shift_label == "shift3_"

  
def test_calculate():
  """ This is an abstract class, so these methods should raise an error """
  feature = Feature(shift=0)

  with pytest.raises(NotImplementedError):
    feature.calculate(None)

def test_result_when_calculate_is_not_defined():
  feature = Feature()
  with pytest.raises(NotImplementedError):
    feature.calculate(None)

def test_result_when_calculate_is_defined():
  """
  Methods are not automatically bound to object instances.
  so we have to do it ourselves
  See :
  http://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object
  """

  feature = Feature()

  def calculator(_, data):
    """
      Calculate the meaning of foo
    """
    return data + ": Foo Bar"

  feature.calculate = types.MethodType(calculator, feature)
  assert feature.calculate("foo") == "foo: Foo Bar"
