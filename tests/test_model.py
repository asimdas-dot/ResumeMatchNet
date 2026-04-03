# Location: ResumeMatchNet/tests/test_model.py

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.resume_matchnet import ResumeMatchNet

class TestResumeMatchNet:
    
    def setup_method(self):
        self.model = ResumeMatchNet()
    
    def test_model_initialization(self):
        """Test model initializes correctly"""
        assert self.model.skill_weight == 0.4
        assert self.model.text_weight == 0.6
        assert self.model.vectorizer is None
    
    def test_extract_skills(self):
        """Test skill extraction"""
        text = "I know Python, Java, and SQL"
        skills = self.model.extract_skills(text)
        assert 'python' in skills
        assert 'java' in skills
        assert 'sql' in skills
    
    def test_compute_similarity(self):
        """Test similarity computation"""
        text1 = "python developer django"
        text2 = "python developer django"
        similarity = self.model.compute_similarity(text1, text2)
        assert similarity >= 0.9
    
    def test_match_function(self, sample_resume, sample_job):
        """Test complete matching function"""
        result = self.model.match(sample_resume, sample_job)
        
        # Check result structure
        assert 'match_score' in result
        assert 'text_similarity' in result
        assert 'skill_match_score' in result
        assert 'matched_skills' in result
        assert 'missing_skills' in result
        
        # Check score ranges
        assert 0 <= result['match_score'] <= 100
        assert 0 <= result['text_similarity'] <= 100
        assert 0 <= result['skill_match_score'] <= 100
    
    def test_high_match_score(self):
        """Test high similarity scenario"""
        resume = "Python Django SQL Developer"
        job = "Need Python Django SQL Developer"
        result = self.model.match(resume, job)
        assert result['match_score'] > 50
    
    def test_low_match_score(self):
        """Test low similarity scenario"""
        resume = "Java Spring Boot Developer"
        job = "Python Django SQL Developer"
        result = self.model.match(resume, job)
        # Should have low match because no skill overlap
        assert result['skill_match_score'] < 50