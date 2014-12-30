"""
    Currency Pair Model
"""

from __future__ import print_function
from sqlalchemy.orm import relationship

from datamaker.db.base import Base

from sqlalchemy import Column, Integer, String, Float

import json

from datamaker.data.historical import HistoricalIterator

import pandas as pd
import numpy as np

# pylint: disable=C0103,W0232,C0111,W0142


class CurrencyPair(Base):
    __tablename__ = 'currency_pairs'

    id = Column(Integer, primary_key=True)
    instrument = Column(String, unique=True, index=True)
    pip_value = Column(Float)
    data_sets = relationship("DataSet", backref="currency_pair")

    def __repr__(self):
        return "<CurrencyPair(instrument='{}', pip_value='{}')>".format(
            self.instrument,
            self.pip_value)

    def get_database(self, project_path):
        db_path = project_path / "data" / "historical"
        if not db_path.exists():
            db_path.mkdir()

        return pd.HDFStore(str(db_path / ("%s.h5" % self.instrument)))

    def historical_data(self, project_path):
        try:
            return self._historical_data
        except AttributeError:
            self._historical_data = self.get_database(  # pylint: disable=W0201
                project_path).get("ohlcv")
            return self._historical_data

    def download_historical_data(self, project_path, years):
        """ Get historical data and save it to a database """
        database = self.get_database(project_path)

        for chunk in HistoricalIterator(self.instrument, years):
            print(chunk)
            index = [np.datetime64(x["time"]) for x in chunk.candles]
            database.append("ohlcv", pd.DataFrame(chunk.candles, index=index))

        database.close()

    @staticmethod
    def load(project_path):
        """ Load default currency pairs if they do not exist in the database """

        session = db.Session()

        pairs = json.load((project_path / "currency_pairs.json").open())

        for pair in pairs:
            existing = session.query(CurrencyPair).filter_by(
                instrument=pair["instrument"]).first()
            if existing is None:
                session.add(CurrencyPair(**pair))
        session.commit()
        return session.query(CurrencyPair).all()
