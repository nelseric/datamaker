""" Dataset and feature calculation """

from __future__ import print_function

from sqlalchemy import Column, Integer, ForeignKey

from datamaker.db.base import Base
from datamaker.db import Session, CurrencyPair, FeatureSet

import pandas as pd

import IPython


# pylint: disable=C0103,W0232,C0111,W0142

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
        historical.drop(["complete", "time"], axis=1, inplace=True)

        session = Session()
        session.add(self)

        group_data = None

        for feature in self.feature_set.features:
            print(feature)
            feature_data = feature.load().calculate(historical)
            print("calculated")
            if group_data is None:
                group_data = feature_data
            else:
                group_data = group_data.join(feature_data)
            print("done")
        IPython.embed()

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
