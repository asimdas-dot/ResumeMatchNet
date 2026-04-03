# Location: ResumeMatchNet/tests/test_feature_extraction.py

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.features.tfidf_extractor import TfidfExtractor

class TestFeatureExtraction:
    
    def setup_method(self):
        self.extractor = TfidfExtractor()
    
    def test_tfidf_vectorization(self):
        """Test TF-IDF vectorizer works"""
        documents = ["python developer", "java developer"]
        vectors = self.extractor.fit_transform(documents)
        assert vectors.shape[0] == 2  # Two documents
        assert vectors.shape[1] > 0   # Has features
    
    def test_vectorizer_fitted(self):
        """Test vectorizer fitted state"""
        documents = ["test document"]
        self.extractor.fit_transform(documents)
        assert self.extractor.is_fitted == True
    
    def test_transform_new_document(self):
        """Test transforming new document"""
        documents = ["python developer"]
        self.extractor.fit_transform(documents)
        
        new_doc = ["java developer"]
        vector = self.extractor.transform(new_doc)
        assert vector.shape[0] == 1