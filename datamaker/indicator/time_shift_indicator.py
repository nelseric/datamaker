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

def calculate(data, shiftList = []):
    outLabel = []
    outData = []
    if (len(shiftList) == 0):
        return outData
    
    for n in shiftList:
        outData.append(data[n[0]].shift(n[1]))
        outLabel.append('TS_' + n[0] + '_'  + str(n[1]))
    
    outData = pd.concat(outData, axis=1, keys= outLabel )

    return outData
