import os
import scipy
import numpy as np
import pandas as pd

from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


DIR = os.path.abspath(os.path.dirname(__file__))


class Preprocessor(TransformerMixin):

    def __init__(self, num_features: list, cat_features: list):
        """
        Create preprocessing pipeline

        Parameters
        ----------
        num_features: list
            Numeric features to use
        cat_features: list
            Categorical features to use

        """
        # Features
        self.raw_num_features = list(num_features)
        self.raw_cat_features = list(cat_features)
        self.raw_features = self.raw_num_features + self.raw_cat_features
        # Pipelines
        num_pipeline = Pipeline([
            ('simple_imputer', SimpleImputer()),
            ('std_scaler', StandardScaler())
        ])
        cat_pipeline = Pipeline([
            ('cat_imputer', SimpleImputer(
                strategy="most_frequent",
                missing_values=None
            )),
            ('one_hot_encoder', OneHotEncoder())
        ])
        self.preprocessing_pipeline = ColumnTransformer([
            ('num', num_pipeline, self.raw_num_features),
            ('cat', cat_pipeline, self.raw_cat_features)
        ])

    def all_features(X):
        """Create Preprocessor object using all dataset features"""
        num_features = list(
            X.select_dtypes(include=[np.number])
            .columns
            .astype(str)
            .values
        )
        cat_features = list(
            X.select_dtypes(exclude=[np.number])
            .columns
            .astype(str)
            .values
        )
        return Preprocessor(num_features, cat_features)

    def fit(self, X: pd.DataFrame, y=None):
        """Fit the preprocessing pipeline to the training data"""
        X = X[self.raw_features].copy()
        self.preprocessing_pipeline.fit(X)
        return self

    def transform(self, X: pd.DataFrame, y=None):
        """Return preprocessed data"""
        X = X[self.raw_features].copy()
        X_pp = self.preprocessing_pipeline.transform(X)
        if isinstance(X_pp, scipy.sparse.csr.csr_matrix):
            X_pp = X_pp.toarray()
        X_pp = pd.DataFrame(X_pp, columns=self.get_feature_names())
        return X_pp

    def get_feature_names(self):
        """Return feature names after preprocessing

        Replicates the ``get_feature_names`` function in the sklearn
        Transformer classes

        """
        num_features = list(self.raw_num_features)
        cat_features = list(
            self.preprocessing_pipeline
            .named_transformers_['cat']
            .named_steps['one_hot_encoder']
            .get_feature_names(self.raw_cat_features)
        )
        return num_features + cat_features
