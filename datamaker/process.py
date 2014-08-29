import sys
import os.path

import pandas as pd

import pyximport; pyximport.install()

import datamaker.result.should_buy as should_buy

import datamaker.indicator.EWMA_indicator as EWMA_ind

import datamaker.indicator.time_shift_indicator as ts_ind

import IPython


def generate_outputs():
  if not len(sys.argv) > 1:
    print "Please provide input database"
    exit(1)

  input_file_name = sys.argv[1]

  if not os.path.isfile(input_file_name):
    print "Please provide input database"
    exit(1)

  store = pd.HDFStore(input_file_name)

  print "Loading 'ticks_ohlcv'"
  data = store.get('ticks_ohlcv')

  print "Applying should_buy"
  data["should_buy"] = should_buy.apply(data.values, 0.00055, 0.00015, 1440)
  
  store.put('ticks_ohlcv', data)

  store.close()
  
def generate_indicators():
  if not len(sys.argv) > 1:
    print "Please provide input database"
    exit(1)

  input_file_name = sys.argv[1]

  if not os.path.isfile(input_file_name):
    print "Please provide input database"
    exit(1)

  store = pd.HDFStore(input_file_name)

  print "Loading 'ticks_ohlcv'"
  data = store.get('ticks_ohlcv')

  print "Applying ewma indicator calculation"
  indicatorData = EWMA_ind.calculate(data, 5)
  
  print "Applying timeshift indicator calculator"
  tsList = [["EWMA_span_5", 5], ["EWMA_span_5", 10]]
  indicatorData = indicatorData.join(ts_ind.calculate(indicatorData, tsList))
  
  store.put('indicator_data', indicatorData)
  #store.put('ticks_ohlcv', data)

  store.close()


def shell():
  if not len(sys.argv) > 1:
    print "Please provide input database"
    exit(1)

  input_file_name = sys.argv[1]

  if not os.path.isfile(input_file_name):
    print "Please provide input database"
    exit(1)

  store = pd.HDFStore(input_file_name)

  print "Loading 'ticks_ohlcv'"
  data = store.get('ticks_ohlcv')
  
  IPython.embed()

  store.close()

if __name__=='__main__':
    generate_indicators()
