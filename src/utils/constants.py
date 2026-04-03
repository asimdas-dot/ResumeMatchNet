# Location: C:\Users\asim2\Desktop\ResumeMatchNet\src\utils\constants.py

# Job Database
JOB_DATABASE = {
    "Software Engineer - Python": """
    Looking for Python Developer with Django and SQL
    Required Skills: Python, Django, SQL, REST APIs, Git
    Experience: 2+ years
    """,
    
    "Data Scientist": """
    Hiring Data Scientist with Python and Machine Learning
    Required Skills: Python, pandas, scikit-learn, TensorFlow, SQL
    Experience: 3+ years
    """,
    
    "Java Backend Developer": """
    Seeking Java Developer with Spring Boot experience
    Required Skills: Java, Spring Boot, Microservices, MySQL, Hibernate
    Experience: 3+ years
    """,
    
    "Frontend React Developer": """
    Looking for React Developer with modern JavaScript
    Required Skills: React, JavaScript, HTML5, CSS3, Redux
    Experience: 2+ years
    """,
    
    "DevOps Engineer": """
    Hiring DevOps Engineer with cloud experience
    Required Skills: AWS, Docker, Kubernetes, Jenkins, Terraform
    Experience: 3+ years
    """,
    
    "Full Stack Developer": """
    Seeking Full Stack Developer with versatile skills
    Required Skills: Python/Node.js, React, SQL, Git, REST APIs
    Experience: 3+ years
    """,
    
    "Machine Learning Engineer": """
    Hiring ML Engineer for AI projects
    Required Skills: Python, TensorFlow/PyTorch, scikit-learn, Deep Learning
    Experience: 2+ years
    """,
    
    "Data Analyst": """
    Looking for Data Analyst for business intelligence
    Required Skills: SQL, Excel, Tableau/Power BI, Python
    Experience: 1+ years
    """
}

# Skill database
SKILL_DATABASE = {
    'python', 'java', 'javascript', 'sql', 'django', 'flask', 'tensorflow',
    'pytorch', 'pandas', 'numpy', 'scikit-learn', 'aws', 'docker', 'kubernetes',
    'react', 'angular', 'spring', 'mongodb', 'postgresql', 'mysql', 'git',
    'jenkins', 'terraform', 'redux', 'html', 'css', 'rest api', 'microservices'
}

# Model configuration
MODEL_CONFIG = {
    'skill_weight': 0.4,
    'text_weight': 0.6,
    'max_features': 1000,
    'ngram_range': (1, 2)
}

# File paths
DATA_PATHS = {
    'raw_data': './data/raw/',
    'processed_data': './data/processed/',
    'models': './models/'
}