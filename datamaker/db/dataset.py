""" Dataset and feature calculation """

from __future__ import print_function

from sqlalchemy import Column, Integer, ForeignKey

from datamaker.db.base import Base
from datamaker.db import Session, CurrencyPair, FeatureSet, Feature

import pandas as pd
import numpy as np

import IPython

# pylint: disable=C0103,W0232

class DataSet(Base):
    __tablename__ = "data_sets"

    feature_set_id = Column(
        Integer, ForeignKey('feature_sets.id'), primary_key=True)
    currency_pair_id = Column(
        Integer, ForeignKey('currency_pairs.id'), primary_key=True)

    def generate(self, project_path):
        """
            Calculate all features in this dataset with the currency pair's historical data
        """

        # pylint: disable=E1101

        historical = self.currency_pair.historical_data(project_path)

        session = Session()

        features = session.query(Feature).filter_by(
            feature_set=self.feature_set)

        for feature in features:
            feature_path = self.currency_pair.feature_path(project_path) / (feature.key() + ".npy")
            print(feature_path)
            if not feature_path.exists():
                feature_data = feature.load_calculator().calculate(historical)
                print("Calculated")
                util.save_pandas(str(feature_path), feature_data)
                print("Stored")
            else:
                print("Cached")

    @staticmethod
    def load(ds_dicts, session=Session()):
        """
            Create a dataset from a dict, if the dataset specified doesn't exist
        """
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
