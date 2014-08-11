__author__ = "Eric Nelson"


import datetime

def np_minute(tm):
  return tm - datetime.timedelta(seconds=tm.second,
                                 microseconds=tm.microsecond)
