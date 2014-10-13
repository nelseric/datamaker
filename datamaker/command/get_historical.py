"""
@author: Eric Nelson
"""
from __future__ import print_function
import pandas as pd
import argparse as ap

import dotenv
import ext.oandapy as oandapy
import os

import datetime

# pylint: disable=W0612

def get_historical_data():
  """
    Load historical data from OANDA, making as many requests as required
  """

  dotenv.load_dotenv('.env')
  parser = ap.ArgumentParser(description='Run an experiment')
  parser.add_argument('instrument', type=str,
                      help='OANDA Currency Pair Instrument')
  parser.add_argument('granularity', type=str,
                      help='Candlestick Granularity')  

  parser.add_argument('range', type=float,
                      help='The range in years to get')  

  parser.add_argument('output_file', type=ap.FileType('w'),
                      help='Output OHLCV HDF5 Store')
  args = parser.parse_args()
  store = pd.HDFStore(args.output_file.name)  

  data_range = datetime.timedelta(365.25 * args.range)

  data_start = datetime.datetime.now() - data_range

  # oanda_acct = os.environ.get("OANDA_ACCOUNT", "")
  oanda_token = os.environ.get("OANDA_TOKEN", "")
  oanda_env = os.environ.get("OANDA_ENV", "")
  oanda = oandapy.API(environment=oanda_env, access_token=oanda_token)

  cur_date = data_start.isoformat()

  print(cur_date)
  cur = oanda.get_history(instrument=args.instrument,
                          granularity=args.granularity,
                          count=5000,
                          start=cur_date)
  cur = _decode_dict(cur)

  index = pd.tseries.index.DatetimeIndex([x['time'] for x in cur["candles"]])
  data = pd.DataFrame(cur["candles"], index=index)
  store.put("ohlcv", data, append=True, format="table")

  cur_date = data["time"][-1]
  print(len(data))

  while len(cur['candles']) >= 4999:
    print(cur_date)
    cur = oanda.get_history(instrument=args.instrument,
                            granularity=args.granularity,
                            count=5000,
                            start=cur_date)
    cur = _decode_dict(cur)
    cur["candles"] = cur["candles"][1:]
    
    index = pd.tseries.index.DatetimeIndex([x['time'] for x in cur["candles"]])
    cur_data = pd.DataFrame(cur["candles"], index=index)

    store.put("ohlcv", cur_data, append=True, format="table")
    cur_date = cur_data["time"][-1]


  import IPython
  IPython.embed()
  

  store.close()

def _decode_list(data):
  rv = []
  for item in data:
    if isinstance(item, unicode):
      item = item.encode('utf-8')
    elif isinstance(item, list):
      item = _decode_list(item)
    elif isinstance(item, dict):
      item = _decode_dict(item)
    rv.append(item)
  return rv
def _decode_dict(data):
  rv = {}
  for key, value in data.iteritems():
    if isinstance(key, unicode):
      key = key.encode('utf-8')
    if isinstance(value, unicode):
      value = value.encode('utf-8')
    elif isinstance(value, list):
      value = _decode_list(value)
    elif isinstance(value, dict):
      value = _decode_dict(value)
    rv[key] = value
  return rv
