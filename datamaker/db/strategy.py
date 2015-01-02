""" Strategy """

from __future__ import print_function

from sqlalchemy import Column, Integer, String, PickleType, ForeignKey, Table, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from datamaker.db.base import Base

from datamaker.db import DataSet

import pandas as pd
import numpy as np

import IPython

# pylint: disable=C0103,W0232,C0111,W0142,E1101


class StrategyDataSet(Base):
    __tablename__ = "strategies_datasets"
    strategy_id = Column(Integer, ForeignKey("strategies.id"), primary_key=True)
    currency_pair_id = Column(Integer, primary_key=True)
    feature_set_id = Column(Integer, primary_key=True)
    __table_args__ = (ForeignKeyConstraint([currency_pair_id, feature_set_id],
                                           [DataSet.currency_pair_id, DataSet.feature_set_id]),
                      {})


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True)
    currency_pair_id = Column(
        Integer, ForeignKey('currency_pairs.id'), primary_key=True)

    strategy = Column(String)
    heuristic = Column(String)
    heuristic_parameters = Column(PickleType)

    data_sets = relationship(
        "DataSet", secondary=StrategyDataSet.__table__, backref="strategies")

    @staticmethod
    def load(strategy_dict):
        IPython.embed()
        
