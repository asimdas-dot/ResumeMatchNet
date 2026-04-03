# Location: ResumeMatchNet/tests/test_preprocessing.py

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing.cleaner import TextCleaner

class TestPreprocessing:
    
    def setup_method(self):
        self.cleaner = TextCleaner()
    
    def test_clean_text_lowercase(self):
        """Test text is converted to lowercase"""
        result = self.cleaner.clean_text("HELLO World")
        assert result == "hello world"
    
    def test_clean_text_remove_special_chars(self):
        """Test special characters are removed"""
        result = self.cleaner.clean_text("Python!!! Developer @#$%")
        assert "!" not in result
        assert "@" not in result
        assert "#" not in result
    
    def test_remove_stopwords(self):
        """Test stopwords removal"""
        result = self.cleaner.remove_stopwords("this is a python developer")
        assert "python" in result
        assert "developer" in result
    
    def test_preprocess_document(self):
        """Test complete preprocessing pipeline"""
        text = "Python Developer!!! Need 5+ years experience."
        result = self.cleaner.preprocess(text)
        assert "python" in result
        assert "developer" in result
        assert "years" not in result  # Should be removed?
    
    def test_empty_text(self):
        """Test empty text handling"""
        result = self.cleaner.clean_text("")
        assert result == ""