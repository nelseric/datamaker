# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 14:13:25 2014

@author: nater
"""

import numpy as np
import pandas as pd

# 0 Ask         open            1.084150
# 1             high            1.084150
# 2             low             1.083600
# 3             close           1.083900
# 4 Bid         open            1.084000
# 5             high            1.084000
# 6             low             1.083250
# 7             close           1.083350
# 8 Bid Volume  Ask volume     70.700001
# 9 Ask Volume  Bid volume    124.599999

def apply(data, spanArg = 20):
    
    #outData = np.zeros((len(data),1))
    
    outData = pd.ewma(data["Ask_open"], span=spanArg)
    outData = pd.DataFrame(outData, columns= ['EWMA_span_'+str(spanArg)])

    return outData
