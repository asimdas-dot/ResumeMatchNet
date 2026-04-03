# Location: ResumeMatchNet/tests/conftest.py

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def sample_resume():
    """Sample resume for testing"""
    return """
    John Doe
    Software Engineer with 5 years Python experience
    Skills: Python, Django, SQL, Machine Learning
    """

@pytest.fixture
def sample_job():
    """Sample job description for testing"""
    return """
    Looking for Python Developer with Django and SQL
    Machine Learning experience is a plus
    """

@pytest.fixture
def sample_resume_skills():
    """Sample extracted skills"""
    return {'python', 'django', 'sql', 'machine learning'}

@pytest.fixture
def sample_job_skills():
    """Sample job required skills"""
    return {'python', 'django', 'sql', 'aws'}