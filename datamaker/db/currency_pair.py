"""
    Currency Pair Model
"""

from __future__ import print_function
from sqlalchemy.orm import relationship

from datamaker.db.base import Base

from datamaker.db import Session

from sqlalchemy import Column, Integer, String, Float

import json

from datamaker.data.historical import HistoricalIterator

import pandas as pd
import numpy as np


# pylint: disable=C0103,W0232


class CurrencyPair(Base):

    """
        Definition of a currency pair. Only has instrument,
         and pip value (value of a pip in base currency)
    """
    __tablename__ = 'currency_pairs'

    id = Column(Integer, primary_key=True)
    instrument = Column(String, unique=True, index=True)
    pip_value = Column(Float)
    data_sets = relationship("DataSet", backref="currency_pair")
    strategies = relationship("Strategy", backref="currency_pair")

    # Memoization 
    _historical_data = None

    def __repr__(self):
        return "<CurrencyPair(instrument='{}', pip_value='{}')>".format(
            self.instrument,
            self.pip_value)

    def get_historical_database(self, project_path):
        """ HDF5 store that holds historical data """

        db_path = project_path / "data" / "historical"
        if not db_path.exists():
            db_path.mkdir(parents=True)

        return pd.HDFStore(str(db_path / ("%s.h5" % self.instrument)))

    def historical_data(self, project_path):
        """ loads historical the historical DataFrame, and memoizes it """
        if self._historical_data is None:
            self._historical_data = self.get_historical_database( 
                project_path).get("ohlcv")
        return self._historical_data

    def download_historical_data(self, project_path, years):
        """ Get historical data and save it to a database """
        database = self.get_historical_database(project_path)

        for chunk in HistoricalIterator(self.instrument, years):
            print(chunk)
            index = [np.datetime64(x["time"]) for x in chunk.candles]

            chunk_frame = pd.DataFrame(chunk.candles, index=index)
            chunk_frame.drop(["complete", "time"], axis=1, inplace=True)

            database.append("ohlcv", chunk_frame)

        database.close()

    @staticmethod
    def load(project_path):
        """ Load default currency pairs if they do not exist in the database """

        session = Session()

        pairs = json.load((project_path / "currency_pairs.json").open())

        for pair in pairs:
            existing = session.query(CurrencyPair).filter_by(
                instrument=pair["instrument"]).first()
            if existing is None:
                session.add(
                    CurrencyPair(instrument=pair["instrument"],
                                 pip_value=pair["pip_value"]))
        session.commit()
        return session.query(CurrencyPair).all()
