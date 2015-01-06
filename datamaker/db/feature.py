""" Features and Feature Sets """
from __future__ import print_function
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, PickleType, ForeignKey

from datamaker.db.base import Base
from datamaker.db import Session

# pylint: disable=C0103,W0232,E1101


class FeatureSet(Base):

    """
        Defines a set of common features that may be used together
    """

    __tablename__ = "feature_sets"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    features = relationship("Feature", backref="feature_set")
    data_sets = relationship("DataSet", backref="feature_set")

    @staticmethod
    def load(fs_dict):
        """
            Loads or creates a FeatureSet from a dict, which was loaded from json  
            Also loads each feature.
        """

        session = Session()
        existing = session.query(FeatureSet).filter_by(
            name=fs_dict["name"]).first()
        if existing is not None:
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
    """ Database representation of a feature calculator and its parameters """
    __tablename__ = "features"
    id = Column(Integer, primary_key=True)
    feature_class = Column(String)
    parameters = Column(PickleType)
    feature_set_id = Column(Integer, ForeignKey('feature_sets.id'))

    def load_calculator(self):
        """ 
            Loads the features calculator class from its feature_class string,
            and instantiates it with the features parameters
        """

        split_path = self.feature_class.split(".")
        module = __import__('.'.join(split_path[:-1]), fromlist=[''])
        klass = getattr(module, split_path[-1])
        return klass(**self.parameters)

    def key(self):
        """
            Unique identifer for this feeature, used to look up a
             calculated feature in a  currency pair's feature store
        """
        params_list = [
            "{}={}".format(key, self.parameters[key]) for key in self.parameters]
        params = ",".join(params_list)
        return "{}({})".format(self.feature_class, params)

    def __repr__(self):
        return "{}:{}".format(self.feature_set.name, self.key())
