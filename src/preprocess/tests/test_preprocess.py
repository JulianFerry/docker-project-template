import os
import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer

from pandas.testing import assert_frame_equal

from preprocess import Preprocessor


TEST_DIR = os.path.dirname(__file__)


class TestPreprocessor:
    
    X = pd.DataFrame({
        'A': [1, 2, 3, None, 5],
        'B': ['dog', 'cat', 'mouse', None, 'cat'],
        'C': ['this', 'column', 'is', 'irrelevant', '.']
    })

    def test_init(self):
        """Test that the preprocessor creates a columntransformer pipeline"""
        pp = Preprocessor(num_features=['A'], cat_features=['B'])
        pipeline = pp.preprocessing_pipeline
        assert isinstance(pipeline, ColumnTransformer)
        assert pipeline.transformers[0][0] == 'num'
        assert pipeline.transformers[1][0] == 'cat'
        assert pipeline.transformers[0][1].steps[0][0] == 'simple_imputer'
        assert pipeline.transformers[1][1].steps[1][0] == 'one_hot_encoder'

    def test_all_features(self):
        """Test that the preprocessor can initialise using all features"""
        pp = Preprocessor.all_features(self.X)
        assert pp.raw_num_features == ['A']
        assert pp.raw_cat_features == ['B', 'C']

    def test_fit(self):
        """Test that the preprocessor can fit to a dataset"""
        pp = Preprocessor(num_features=['A'], cat_features=['B'])
        pp.fit(self.X)
        # The `named_transformers_` attribute only exists for fitted pipelines
        assert 'num' in pp.preprocessing_pipeline.named_transformers_
        assert 'cat' in pp.preprocessing_pipeline.named_transformers_
    
    def test_get_feature_names(self):
        """Test that the OHE feature names are added to the feature names"""
        with open(os.path.join(TEST_DIR, 'files/pp_fit.pkl'), 'rb') as f:
            pp = pickle.load(f)
        assert pp.get_feature_names() == ['A', 'B_cat', 'B_dog', 'B_mouse']

    def test_transform(self):
        """Test that a fitted preprocessor transforms the input dataset"""
        with open(os.path.join(TEST_DIR, 'files/pp_fit.pkl'), 'rb') as f:
            pp = pickle.load(f)
        X_pp = pd.DataFrame(
            [[-1.322876, 0.0, 1.0, 0.0],
             [-0.566947, 1.0, 0.0, 0.0],
             [0.188982, 0.0, 0.0, 1.0],
             [0.000000, 1.0, 0.0, 0.0],
             [1.700840, 1.0, 0.0, 0.0]],
            columns = ['A', 'B_cat', 'B_dog', 'B_mouse']
        )
        assert_frame_equal(pp.transform(self.X), X_pp)
        