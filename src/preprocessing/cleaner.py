# src/preprocessing/cleaner.py
import re
import nltk

class TextCleaner:
    def clean_text(self, text):
        """Remove special characters, lowercase"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text
    
    def remove_stopwords(self, text):
        """Remove stopwords"""
        pass