""" Strategy """

from __future__ import print_function

from sqlalchemy import Column, Integer, String, PickleType, ForeignKey, Table, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from datamaker.db.base import Base

from datamaker.db import DataSet, Session, CurrencyPair

import datamaker.util as util

import pandas as pd
import numpy as np

import IPython

import gzip

# pylint: disable=C0103,W0232,C0111,W0142,E1101


class StrategyDataSet(Base):
    __tablename__ = "strategies_datasets"
    strategy_id = Column(
        Integer, ForeignKey("strategies.id"), primary_key=True)
    currency_pair_id = Column(Integer, primary_key=True)
    feature_set_id = Column(Integer, primary_key=True)
    __table_args__ = (ForeignKeyConstraint([currency_pair_id, feature_set_id],
                                           [DataSet.currency_pair_id, DataSet.feature_set_id]),
                      {})


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    currency_pair_id = Column(Integer, ForeignKey('currency_pairs.id'))
    evaluator_class = Column(String)
    heuristic_class = Column(String)
    model_class = Column(String)
    parameters = Column(PickleType)

    data_sets = relationship(
        "DataSet", secondary=StrategyDataSet.__table__, backref="strategies")

    def get_training_data_path(self, project_path):
        """ Path of where to store training data """

        db_path = project_path / "data" / "training"
        if not db_path.exists():
            db_path.mkdir()

        return str(db_path / ("%s.npy" % self.__file_repr__()))

    def get_heuristic_path(self, project_path):
        """ Path of where to store training data """

        db_path = project_path / "data" / "heuristic"
        if not db_path.exists():
            db_path.mkdir()

        return str(db_path / ("%s.npy" % self.__file_repr__()))

    def calculate_training_data(self, project_path):
        """ Joins all data sets toegether, and saves them as one dataframe """

        base = None

        for data_set in self.data_sets:
            ds_features = []
            print(data_set)
            historical = data_set.currency_pair.historical_data(project_path)
            for feature in data_set.feature_set.features:
                print(feature)
                ds_features.append(feature.calculate(historical))

            if base is not None:
                base = base.join(
                    pd.concat(ds_features, axis=1, copy=False),
                    rsuffix=data_set.currency_pair.instrument)
            else:
                base = pd.concat(ds_features, axis=1, copy=False)

        print("Saving")
        util.save_pandas(self.get_training_data_path(project_path), base)
        

    def load_features(self, path):
        """ Loads the joined training dataset """
        return util.load_pandas(self.get_training_data_path(path))

    def heuristic(self):
        """ Loads and configures the heuristic calculator class """
        split_path = self.heuristic_class.split(".")
        module = __import__('.'.join(split_path[:-1]), fromlist=[''])
        klass = getattr(module, split_path[-1])
        return klass(
            take_profit=(
                self.parameters["take_profit"] * self.currency_pair.pip_value),
            stop_loss=(
                self.parameters["stop_loss"] * self.currency_pair.pip_value),
            search_limit=self.parameters.get("search_limit", 14400))

    def evaluator(self):
        """ Loads and configures the heuristic calculator class """
        split_path = self.evaluator_class.split(".")
        module = __import__('.'.join(split_path[:-1]), fromlist=[''])
        klass = getattr(module, split_path[-1])

        return klass(
            take_profit=(
                self.parameters["take_profit"] * self.currency_pair.pip_value),
            stop_loss=(
                self.parameters["stop_loss"] * self.currency_pair.pip_value),
            side=self.parameters["side"])

    def calculate_heuristic(self, path):
        """ Calculates and saves the heuristic to a dataframe """
        data = self.heuristic().calculate(
            self.currency_pair.historical_data(path))
        util.save_pandas(self.get_heuristic_path(path), data)

        
        input_data = self.load_features(path)

        total_data = input_data.join(data)

        with gzip.GzipFile(self.get_heuristic_path(path) + '.csv.gz',
                           mode='w', compresslevel=9) as gzfile:
            total_data.to_csv(gzfile)

    def load_heuristic(self, path):
        """ Loads the heuristic dataframe """
        return util.load_pandas(self.get_heuristic_path(path))

    @staticmethod
    def load(strategy_dict):
        session = Session()
        strategy = session.query(Strategy).filter_by(
            name=strategy_dict["name"]).first()
        if strategy is None:
            currency_pair = session.query(CurrencyPair).filter_by(
                instrument=strategy_dict["instrument"]).first()
            strategy = Strategy(
                name=strategy_dict["name"],
                currency_pair_id=currency_pair.id,
                evaluator_class=strategy_dict["evaluator_class"],
                heuristic_class=strategy_dict["heuristic_class"],
                model_class=strategy_dict["model_class"],
                parameters=strategy_dict["parameters"])

        session.add(strategy)
        strategy.data_sets = DataSet.load(strategy_dict["data_sets"], session)
        session.commit()

    def __repr__(self):
        params_list = [
            "{}={}".format(key, self.parameters[key])
            for key in self.parameters
        ]
        params = ",".join(params_list)

        return "<{}:{}:{}({})>".format(
            self.evaluator_class,
            self.currency_pair.instrument,
            self.heuristic_class,
            params)

    def __file_repr__(self):
        return self.name
