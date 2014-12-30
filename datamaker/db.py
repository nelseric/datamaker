""" SQLite ORM"""
from __future__ import print_function
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

from sqlalchemy import Column, Integer, String, Float, PickleType, ForeignKey

import json


from datamaker.data.historical import HistoricalIterator
import pandas as pd
import numpy as np

# pylint: disable=C0103,W0232,C0111,W0142

engine = create_engine('sqlite:///data/meta.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


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
            self._historical_data = self.get_database(
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

        session = Session()

        pairs = json.load((project_path / "currency_pairs.json").open())

        for pair in pairs:
            existing = session.query(CurrencyPair).filter_by(
                instrument=pair["instrument"]).first()
            if existing == None:
                session.add(CurrencyPair(**pair))
        session.commit()
        return session.query(CurrencyPair).all()


class DataSet(Base):
    __tablename__ = "data_sets"

    feature_set_id = Column(
        Integer, ForeignKey('feature_sets.id'), primary_key=True)
    currency_pair_id = Column(
        Integer, ForeignKey('currency_pairs.id'), primary_key=True)

    def get_database(self, project_path):
        db_path = project_path / "data" / "dataset"
        if not db_path.exists():
            db_path.mkdir()

        return pd.HDFStore(str(db_path / ("%s.h5" % self.currency_pair.instrument)))


    def generate(self, project_path):
        db = self.get_database(project_path)
        historical = self.currency_pair.historical_data(project_path)

    @staticmethod
    def load(ds_dicts):
        session = Session()
        data_sets = []
        for data_set in ds_dicts:
            currency_pair = session.query(CurrencyPair).filter_by(
                instrument=data_set["instrument"]).first()

            feature_set = session.query(FeatureSet).filter_by(
                name=data_set["feature_set"]).first()

            existing = session.query(DataSet).filter_by(
                currency_pair=currency_pair, feature_set=feature_set).first()

            if existing != None:
                data_sets.append(existing)
            else:
                data_set = DataSet(
                    currency_pair=currency_pair, feature_set=feature_set)
                session.add(data_set)
        return data_sets

    def __repr__(self):
        return "<DataSet {}:{}>".format(self.currency_pair.instrument, self.feature_set.name)


class FeatureSet(Base):
    __tablename__ = "feature_sets"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    features = relationship("Feature", backref="feature_set")
    data_sets = relationship("DataSet", backref="feature_set")

    @staticmethod
    def load(fs_dict):

        session = Session()
        existing = session.query(FeatureSet).filter_by(
            name=fs_dict["name"]).first()
        if existing != None:
            return existing

        fs = FeatureSet(name=fs_dict["name"])

        for feature in fs_dict["features"]:
            feature = Feature(feature_class=feature["class"],
                              parameters=feature["parameters"],
                              feature_set=fs)
        session.add(fs)

        session.commit()

        return fs


class Feature(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True)
    feature_class = Column(String)
    parameters = Column(PickleType)
    feature_set_id = Column(Integer, ForeignKey('feature_sets.id'))

    def __repr__(self):
        params_list = [
            "{}={}".format(key, self.parameters[key]) for key in self.parameters]
        params = reduce("{}, {}".format, params_list)
        # params = params_list[0]
        for param in params_list[1:]:
            params = params + ", " + param
        return "{}:{}({})".format(self.feature_set.name, self.feature_class, params)
