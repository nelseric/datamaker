""" Dataset and feature calculation """

from __future__ import print_function

from sqlalchemy import Column, Integer, ForeignKey

from datamaker.db.base import Base
from datamaker.db import Session, CurrencyPair, FeatureSet, Feature

import pandas as pd
import numpy as np

import IPython

import tables
import warnings
warnings.filterwarnings('ignore', category=tables.NaturalNameWarning)


# pylint: disable=C0103,W0232,C0111,W0142,E1101

class DataSet(Base):
    __tablename__ = "data_sets"

    feature_set_id = Column(
        Integer, ForeignKey('feature_sets.id'), primary_key=True)
    currency_pair_id = Column(
        Integer, ForeignKey('currency_pairs.id'), primary_key=True)

    def generate(self, project_path):
        db = self.currency_pair.get_feature_database(project_path)

        historical = self.currency_pair.historical_data(project_path)

        session = Session()

        features = session.query(Feature).filter_by(
            feature_set=self.feature_set)

        for feature in features:
            print(feature)
            if feature.key() not in db:
                feature_data = feature.load().calculate(historical)
                print("Calculated")
                db.put(feature.key(), feature_data)
                print("Stored")
            else:
                print("Cached")

    @staticmethod
    def load(ds_dicts, session=Session()):
        data_sets = []
        for data_set in ds_dicts:
            currency_pair = session.query(CurrencyPair).filter_by(
                instrument=data_set["instrument"]).first()

            feature_set = session.query(FeatureSet).filter_by(
                name=data_set["feature_set"]).first()

            existing = session.query(DataSet).filter_by(
                currency_pair=currency_pair, feature_set=feature_set).first()

            if existing is not None:
                data_sets.append(existing)
            else:
                data_set = DataSet(
                    currency_pair=currency_pair, feature_set=feature_set)
                data_sets.append(data_set)
                session.add(data_set)

        session.commit()
        return data_sets

    def __repr__(self):
        return "<DataSet {}:{}>".format(self.currency_pair.instrument, self.feature_set.name)
