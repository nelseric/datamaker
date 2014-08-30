import pandas as pd
import numpy as np
import random

class EWMAIndicator(object):

    #takes a list of k spans and calculates EWMA
    def __init__(self, data, k):
        super(EWMAIndicator, self).__init__()
        self.data = data['Ask']['open']
        self.span_list = k
        self.outData = pd.DataFrame()
    def calcEWMA(self):
        for span in self.span_list:
            self.outData[str(span) + 'Day EWMA'] = pd.ewma(self.data, span=span)
        return self.outData



