"""
@author: Eric Nelson
"""
import pandas as pd
import argparse
import dotenv
import IPython

def shell():
  """
  Open an IPython shell, with the data set to "data"
  """
  dotenv.load_dotenv('.env')
  parser = argparse.ArgumentParser(description='Open a shell with a database')
  parser.add_argument('store', type=argparse.FileType('w'),
                      help='OHLCV HDF5 Store')
  args = parser.parse_args()

  store = pd.HDFStore(args.store.name)

  IPython.embed()

  store.close()


