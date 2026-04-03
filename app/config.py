import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_CONFIG = {
    'tfidf_max_features': 1000,
    'ngram_range': (1, 2),
    'skill_weight': 0.4,
    'text_weight': 0.6
}

DATA_PATHS = {
    'raw_resumes': BASE_DIR / 'data/raw/resumes.csv',
    'processed_resumes': BASE_DIR / 'data/processed/cleaned_resumes.csv',
    'skill_db': BASE_DIR / 'data/external/skill_database.json'
}