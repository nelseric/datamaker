"""
@author: Eric Nelson

* can be used, but it probably shouldn't
"""
__all__ = ["macd", "ewma", "noop", "bollinger_band",
           "talib_indicators", "stochastic_oscillator"]

class Feature(object):

    """
    Abstract interface for NN feature implementation
    :param shift: The number of records to shift the
                  input foreward, cannot be negative.
    """

    def __init__(self, **kwargs):
        self.shift = kwargs.pop('shift', 0)

        self.input_columns = kwargs.pop('columns', None)

        self._shift_label = "shift{}_".format(self.shift)

    def calculate(self, data):
        """
        Calculate the feature given input data,
        then apply wrapped operations on that data
        """

        if self.input_columns is not None:
            if hasattr(self.input_columns, "__iter__"):
                delcols = data.columns - self.input_columns
                data = data.drop(delcols, axis=1)
            else:
                data = data[self.input_columns]

        if self.shift > 0:
            shifted = self._calculate(data).shift(self.shift)
            shifted.columns = [
                self._shift_label + col for col in shifted.columns]
            return shifted
        else:
            return self._calculate(data)

    def calculate_unshifted(self, data):
        """
        Get the unshifted calculation
        """
        return self._calculate(data)

    def _calculate(self, data):
        """
          The method calculate method must be overwritten
          and should return a dataframe, that does not
          include the base data

        """
        raise NotImplementedError("Your indicator must define this")
