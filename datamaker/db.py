""" SQLite ORM"""
from __future__ import print_function
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String, Float

import json


from datamaker.data.historical import HistoricalIterator
import pandas as pd
import numpy as np


engine = create_engine('sqlite:///data/meta.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class CurrencyPair(Base):
  __tablename__ = 'currency_pairs'
 
  id = Column(Integer, primary_key=True)
  instrument = Column(String, unique=True, index=True)
  pip_value = Column(Float)

  def __repr__(self):
    return "<CurrencyPair(instrument='%s', pip_value='%s')>" %(self.instrument,
                                                               self.pip_value)

  def get_historical(self, dbpath, years):
    """ Get historical data and save it to a database """
    database = pd.HDFStore(str(dbpath / ("%s.h5" % self.instrument)))

    for chunk in HistoricalIterator(self.instrument, years):
      print(chunk)
      index = [np.datetime64(x["time"]) for x in  chunk.candles]
      database.append("ohlcv", pd.DataFrame(chunk.candles, index=index))

    database.close()

  @staticmethod
  def load(path):
    """ Load default currency pairs if they do not exist in the database """

    session = Session()


    pairs = json.load((path / "currency_pairs.json").open())

    for pair in pairs:
      existing = session.query(CurrencyPair).filter_by(instrument=pair["instrument"]).first()
      if existing == None:
        session.add(CurrencyPair(**pair))
    session.commit()
    return session.query(CurrencyPair).all()

