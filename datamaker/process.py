import sys
import os.path

import pandas as pd

import pyximport; pyximport.install()

import datamaker.c_process as op


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
  data["should_buy"] = op.apply_should_buy(data, 0.00055, 0.00015, 1440)

  store.put('ticks_ohlcv', data)

  store.close()
