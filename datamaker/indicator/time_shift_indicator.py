# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 14:13:25 2014

@author: nater
"""

import numpy as np
import pandas as pd

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
