import pandas as pd

class EWMAIndicator(object):
    """takes a list of k spans and calculates Exponential Weighted Moving Average"""
    def __init__(self, data, span_container):
        super(EWMAIndicator, self).__init__()
        self.data = data
        self.span_list = span_container
        self.outData = pd.DataFrame()
        
    def calculate(self):
        for span in self.span_list:
            self.outData[str(span) + 'Day EWMA'] = pd.ewma(self.data, span=span)
        return self.outData
   