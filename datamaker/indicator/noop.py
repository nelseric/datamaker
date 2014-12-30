"""
@author: Eric Nelson
"""
import datamaker.feature as s


class Feature(s.Feature):

    """Sets result to be data"""

    def _calculate(self, data):
        return data
