import database as db
import os
import numpy as np
import pandas as pd
import joblib

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

DIR = os.path.abspath(os.path.dirname(__file__))


class PreProcessor(TransformerMixin):

    def __init__(self):
        """ Defines features to use and creates modelling pipeline """

        # Define features
        self.raw_features = None

        # Create pipelines
        self._init_pipelines()

    def _init_pipelines(self):
        """ Creates modelling pipeline """

        # Full preprocessing pipeline
        self.preprocessing_pipeline = None

    def fit(self, X, y=None):
        """ Fit the preprocessing pipeline to all of the training data """

        # Select features and fit preprocessing
        X = X[self.raw_features].copy()
        self.preprocessing_pipeline.fit(X)
        return self

    def transform(self, X, y=None):
        """ Return preprocessed data """

        # Preproces data
        X = X[self.raw_features].copy()
        X_pp = self.preprocessing_pipeline.transform(X)
        X_pp = pd.DataFrame(X_pp, columns=self.get_feature_names())

        return X_pp

    def get_feature_names(self):
        """
        Feature names after preprocessing.
        Replicates the get_feature_names function in the sklearn Transformer classes.
        """
        return self.raw_features


if __name__ == "__main__":
    from preprocessing import PreProcessor # noqa

    # Load data
    db_config = db.get_config()
    train = db.load(*db_config, 'raw_train')
    X_train = train.drop('SalePrice', axis=1)

    # Fit and transform training data
    pp = PreProcessor()
    X_train_pp = pp.fit_transform(X_train)
    train_pp = X_train_pp.assign(SalePrice=train['SalePrice'])

    # Save preprocessed data and fitted preprocessor
    db.save(train_pp, *db_config, 'processed_train')
    joblib.dump(pp, os.path.join(DIR, '../pickle/PreProcessor.pkl'))
