""" SQLite ORM"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data/meta.db', echo=False)
Session = sessionmaker(bind=engine)

__all__ = ["currency_pair", "dataset", "feature"]

from .currency_pair import CurrencyPair
from .feature import Feature
from .feature import FeatureSet

# import depends on previous (CurrencyPair, FeatureSet)
from .dataset import DataSet
