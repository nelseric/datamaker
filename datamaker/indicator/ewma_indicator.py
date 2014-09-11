import pandas as pd

class EWMAIndicator(object):
    """takes a list of k spans and calculates EWMA"""
    def __init__(self, data, k):
        super(EWMAIndicator, self).__init__()
        self.data = data['Ask_open']
        self.span_list = k
        self.outData = pd.DataFrame()
        
    def calculate(self):
        for span in self.span_list:
            self.outData[str(span) + 'Day EWMA'] = pd.ewma(self.data, span=span)
        return self.outData
   
