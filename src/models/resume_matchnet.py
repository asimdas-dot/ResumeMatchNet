# Location: C:\Users\asim2\Desktop\ResumeMatchNet\src\models\resume_matchnet.py

"""
ResumeMatchNet - Core Matching Engine
-------------------------------------
This module contains the main ResumeMatchNet class for matching
resumes with job descriptions using NLP techniques.
"""

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Set, List, Tuple, Any

# Comprehensive Skill Database
SKILL_DATABASE = {
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
    'swift', 'kotlin', 'php', 'scala', 'r', 'matlab', 'perl', 'html', 'css',
    
    # Frameworks & Libraries
    'django', 'flask', 'fastapi', 'spring', 'spring boot', 'hibernate',
    'react', 'angular', 'vue', 'node.js', 'express', 'jquery', 'bootstrap',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
    'matplotlib', 'seaborn', 'opencv', 'nltk', 'spacy', 'transformers',
    
    # Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'sqlite', 'redis',
    'cassandra', 'elasticsearch', 'dynamodb', 'firebase', 'mariadb',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins',
    'git', 'github', 'gitlab', 'bitbucket', 'ci/cd', 'terraform', 'ansible',
    'prometheus', 'grafana', 'nginx', 'apache', 'linux', 'ubuntu', 'centos',
    
    # Data Science & ML
    'machine learning', 'deep learning', 'nlp', 'natural language processing',
    'computer vision', 'data science', 'data analysis', 'data analytics',
    'statistics', 'tableau', 'power bi', 'excel', 'hadoop', 'spark', 'airflow',
    
    # Web Technologies
    'rest api', 'graphql', 'soap', 'microservices', 'jwt', 'oauth', 'jpa',
    
    # Soft Skills
    'leadership', 'communication', 'problem solving', 'teamwork', 'agile',
    'scrum', 'project management', 'critical thinking', 'time management',
    
    # Certifications & Tools
    'jira', 'confluence', 'slack', 'trello', 'postman', 'swagger', 'intellij',
    'vscode', 'pycharm', 'eclipse', 'visual studio'
}


class ResumeMatchNet:
    """
    Resume-Job Description Matching System
    
    This class provides functionality to match resumes with job descriptions
    using a combination of text similarity (TF-IDF + Cosine Similarity) and
    skill-based matching.
    
    Attributes:
        skill_weight (float): Weight given to skill matching (0-1)
        text_weight (float): Weight given to text similarity (0-1)
        vectorizer (TfidfVectorizer): TF-IDF vectorizer instance
        skill_database (Set): Set of known skills for extraction
    
    Example:
        >>> model = ResumeMatchNet()
        >>> result = model.match(resume_text, job_text)
        >>> print(f"Match Score: {result['match_score']}%")
    """
    
    def __init__(self, skill_weight: float = 0.4, text_weight: float = 0.6, 
                 skill_database: Set = None):
        """
        Initialize the ResumeMatchNet model.
        
        Args:
            skill_weight: Weight for skill matching (default: 0.4)
            text_weight: Weight for text similarity (default: 0.6)
            skill_database: Custom skill database (optional)
        """
        # Validate weights
        if not (0 <= skill_weight <= 1 and 0 <= text_weight <= 1):
            raise ValueError("Weights must be between 0 and 1")
        if abs(skill_weight + text_weight - 1.0) > 0.01:
            raise ValueError("Skill weight + text weight must equal 1.0")
        
        self.skill_weight = skill_weight
        self.text_weight = text_weight
        self.vectorizer = None
        self.skill_database = skill_database if skill_database else SKILL_DATABASE
        self.is_fitted = False
        
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for analysis.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned and preprocessed text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters (keep letters, spaces, hyphens)
        text = re.sub(r'[^a-z\s\-]', '', text)
        
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove common stopwords (optional - can be enhanced)
        stopwords = {'a', 'an', 'the', 'and', 'or', 'but', 'for', 'nor', 'so',
                    'yet', 'of', 'to', 'in', 'on', 'at', 'with', 'without'}
        words = text.split()
        text = ' '.join([w for w in words if w not in stopwords and len(w) > 1])
        
        return text
    
    def extract_skills(self, text: str) -> Set[str]:
        """
        Extract skills from text using dictionary matching.
        
        Args:
            text: Input text (resume or job description)
            
        Returns:
            Set of extracted skills
        """
        if not text:
            return set()
        
        text_lower = text.lower()
        found_skills = set()
        
        # Method 1: Direct word matching
        for skill in self.skill_database:
            # Use word boundary matching for better accuracy
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        # Method 2: Multi-word skill matching (e.g., "machine learning")
        for skill in self.skill_database:
            if ' ' in skill and skill in text_lower:
                found_skills.add(skill)
        
        return found_skills
    
    def extract_skills_batch(self, texts: List[str]) -> List[Set[str]]:
        """
        Extract skills from multiple texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of skill sets
        """
        return [self.extract_skills(text) for text in texts]
    
    def compute_text_similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts using TF-IDF.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        if not text1 or not text2:
            return 0.0
        
        # Preprocess texts
        proc_text1 = self.preprocess_text(text1)
        proc_text2 = self.preprocess_text(text2)
        
        if not proc_text1 or not proc_text2:
            return 0.0
        
        # Create TF-IDF vectors
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        
        try:
            vectors = self.vectorizer.fit_transform([proc_text1, proc_text2])
            similarity = cosine_similarity(vectors[0], vectors[1])
            self.is_fitted = True
            return float(similarity[0][0])
        except Exception as e:
            print(f"Error computing similarity: {e}")
            return 0.0
    
    def compute_skill_score(self, resume_skills: Set[str], job_skills: Set[str]) -> float:
        """
        Compute skill-based matching score.
        
        Args:
            resume_skills: Skills found in resume
            job_skills: Skills required in job description
            
        Returns:
            Skill match score between 0 and 1
        """
        if not job_skills:
            return 0.0
        
        matched_skills = resume_skills.intersection(job_skills)
        score = len(matched_skills) / len(job_skills)
        
        return min(1.0, score)  # Cap at 1.0
    
    def calculate_weighted_score(self, text_similarity: float, skill_score: float) -> float:
        """
        Calculate weighted final score.
        
        Args:
            text_similarity: Text similarity score (0-1)
            skill_score: Skill match score (0-1)
            
        Returns:
            Weighted final score (0-100)
        """
        final_score = (self.text_weight * text_similarity + 
                      self.skill_weight * skill_score) * 100
        
        return round(final_score, 2)
    
    def match(self, resume_text: str, job_text: str) -> Dict[str, Any]:
        """
        Match a resume with a job description.
        
        This is the main method that performs the complete matching pipeline:
        1. Extract skills from both documents
        2. Compute text similarity using TF-IDF
        3. Calculate skill match score
        4. Generate weighted final score
        5. Return detailed analysis
        
        Args:
            resume_text: Resume text content
            job_text: Job description text content
            
        Returns:
            Dictionary containing:
            - match_score: Overall match percentage (0-100)
            - skill_match_score: Skills match percentage (0-100)
            - text_similarity: Text similarity percentage (0-100)
            - matched_skills: List of skills found in both
            - missing_skills: List of job skills not in resume
            - resume_skills: All skills found in resume
            - job_skills: All skills found in job description
            - skill_count: Dictionary with skill counts
            - recommendations: Improvement suggestions
        """
        # Input validation
        if not resume_text or not isinstance(resume_text, str):
            return self._empty_result("Resume text is empty or invalid")
        
        if not job_text or not isinstance(job_text, str):
            return self._empty_result("Job description is empty or invalid")
        
        try:
            # Step 1: Extract skills
            resume_skills = self.extract_skills(resume_text)
            job_skills = self.extract_skills(job_text)
            
            # Step 2: Compute text similarity
            text_similarity = self.compute_text_similarity(resume_text, job_text)
            
            # Step 3: Compute skill score
            skill_score = self.compute_skill_score(resume_skills, job_skills)
            
            # Step 4: Calculate final weighted score
            match_score = self.calculate_weighted_score(text_similarity, skill_score)
            
            # Step 5: Prepare results
            matched_skills = resume_skills.intersection(job_skills)
            missing_skills = job_skills - resume_skills
            
            # Step 6: Generate recommendations
            recommendations = self._generate_recommendations(
                match_score, missing_skills, skill_score
            )
            
            return {
                'match_score': match_score,
                'skill_match_score': round(skill_score * 100, 2),
                'text_similarity': round(text_similarity * 100, 2),
                'matched_skills': sorted(list(matched_skills)),
                'missing_skills': sorted(list(missing_skills)),
                'resume_skills': sorted(list(resume_skills)),
                'job_skills': sorted(list(job_skills)),
                'skill_count': {
                    'resume': len(resume_skills),
                    'job': len(job_skills),
                    'matched': len(matched_skills),
                    'missing': len(missing_skills)
                },
                'recommendations': recommendations,
                'weights_used': {
                    'text_weight': self.text_weight,
                    'skill_weight': self.skill_weight
                }
            }
            
        except Exception as e:
            return self._empty_result(f"Error during matching: {str(e)}")
    
    def match_batch(self, resumes: List[str], job_description: str) -> List[Dict[str, Any]]:
        """
        Match multiple resumes against a single job description.
        
        Args:
            resumes: List of resume texts
            job_description: Job description text
            
        Returns:
            List of match results for each resume
        """
        results = []
        for i, resume in enumerate(resumes):
            result = self.match(resume, job_description)
            result['resume_index'] = i
            results.append(result)
        
        # Sort by match score (highest first)
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results
    
    def compare_jobs(self, resume_text: str, job_descriptions: List[str]) -> List[Dict[str, Any]]:
        """
        Compare a single resume against multiple job descriptions.
        
        Args:
            resume_text: Resume text
            job_descriptions: List of job description texts
            
        Returns:
            List of match results for each job
        """
        results = []
        for i, job in enumerate(job_descriptions):
            result = self.match(resume_text, job)
            result['job_index'] = i
            results.append(result)
        
        # Sort by match score (highest first)
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results
    
    def _generate_recommendations(self, match_score: float, 
                                   missing_skills: Set[str], 
                                   skill_score: float) -> List[str]:
        """
        Generate improvement recommendations.
        
        Args:
            match_score: Overall match score
            missing_skills: Skills missing from resume
            skill_score: Skill match score
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if match_score >= 80:
            recommendations.append("Excellent match! You're highly qualified for this position.")
        elif match_score >= 70:
            recommendations.append("Good match! Minor improvements could make you a top candidate.")
        elif match_score >= 60:
            recommendations.append("Decent match. Consider highlighting relevant skills more prominently.")
        elif match_score >= 50:
            recommendations.append("Moderate match. Review the job requirements and update your resume.")
        else:
            recommendations.append("Low match. Consider gaining experience in required skills.")
        
        if missing_skills and skill_score < 0.5:
            top_missing = list(missing_skills)[:3]
            recommendations.append(f"Add these skills to your resume: {', '.join(top_missing)}")
        
        if match_score < 60:
            recommendations.append("Tailor your resume to include keywords from the job description.")
        
        return recommendations
    
    def _empty_result(self, error_message: str = "") -> Dict[str, Any]:
        """
        Return empty result structure for error cases.
        
        Args:
            error_message: Error description
            
        Returns:
            Empty result dictionary
        """
        return {
            'match_score': 0,
            'skill_match_score': 0,
            'text_similarity': 0,
            'matched_skills': [],
            'missing_skills': [],
            'resume_skills': [],
            'job_skills': [],
            'skill_count': {
                'resume': 0,
                'job': 0,
                'matched': 0,
                'missing': 0
            },
            'recommendations': [error_message] if error_message else [],
            'error': error_message
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the model configuration.
        
        Returns:
            Dictionary with model information
        """
        return {
            'model_name': 'ResumeMatchNet',
            'version': '1.0.0',
            'skill_weight': self.skill_weight,
            'text_weight': self.text_weight,
            'skill_database_size': len(self.skill_database),
            'is_fitted': self.is_fitted,
            'skills_sample': list(self.skill_database)[:20]
        }
    
    def add_skills(self, new_skills: List[str]) -> int:
        """
        Add new skills to the database.
        
        Args:
            new_skills: List of new skills to add
            
        Returns:
            Number of skills added
        """
        added = 0
        for skill in new_skills:
            skill_lower = skill.lower().strip()
            if skill_lower and skill_lower not in self.skill_database:
                self.skill_database.add(skill_lower)
                added += 1
        return added
    
    def remove_skills(self, skills_to_remove: List[str]) -> int:
        """
        Remove skills from the database.
        
        Args:
            skills_to_remove: List of skills to remove
            
        Returns:
            Number of skills removed
        """
        removed = 0
        for skill in skills_to_remove:
            skill_lower = skill.lower().strip()
            if skill_lower in self.skill_database:
                self.skill_database.remove(skill_lower)
                removed += 1
        return removed


# Utility function for quick matching
def quick_match(resume_text: str, job_text: str) -> Dict[str, Any]:
    """
    Quick match function for simple use cases.
    
    Args:
        resume_text: Resume text
        job_text: Job description text
        
    Returns:
        Match results dictionary
    """
    model = ResumeMatchNet()
    return model.match(resume_text, job_text)


# Example usage and testing
if __name__ == "__main__":
    # Test the model
    print("=" * 60)
    print("ResumeMatchNet - Test Run")
    print("=" * 60)
    
    # Sample data
    sample_resume = """
    Python Developer with 5 years experience
    Skills: Python, Django, SQL, Git, Docker
    Built REST APIs and web applications
    """
    
    sample_job = """
    Looking for Python Developer
    Required: Python, Django, SQL, REST APIs
    Experience with Docker is a plus
    """
    
    # Create model instance
    model = ResumeMatchNet()
    
    # Perform matching
    result = model.match(sample_resume, sample_job)
    
    # Display results
    print(f"\n📊 Match Results:")
    print(f"   Overall Match: {result['match_score']}%")
    print(f"   Skills Match: {result['skill_match_score']}%")
    print(f"   Text Similarity: {result['text_similarity']}%")
    
    print(f"\n🔧 Skills Analysis:")
    print(f"   Matched: {result['matched_skills']}")
    print(f"   Missing: {result['missing_skills']}")
    
    print(f"\n💡 Recommendations:")
    for rec in result['recommendations']:
        print(f"   • {rec}")
    
    print(f"\n📈 Skill Statistics:")
    print(f"   Resume Skills: {result['skill_count']['resume']}")
    print(f"   Job Skills: {result['skill_count']['job']}")
    print(f"   Matched: {result['skill_count']['matched']}")
    
    print("\n" + "=" * 60)
    print("✅ Model test completed successfully!")
    print("=" * 60)
    
    # Model info
    info = model.get_model_info()
    print(f"\n📋 Model Information:")
    print(f"   Name: {info['model_name']}")
    print(f"   Version: {info['version']}")
    print(f"   Skill Database: {info['skill_database_size']} skills")