""" Features and Feature Sets """
from __future__ import print_function
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, PickleType, ForeignKey

from datamaker.db.base import Base
from datamaker.db import Session

# pylint: disable=C0103,W0232,C0111,W0142


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
