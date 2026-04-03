# Location: C:\Users\asim2\Desktop\ResumeMatchNet\app\main.py

import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from src.models.resume_matchnet import ResumeMatchNet
from src.utils.file_processor import FileProcessor

# Job Database
JOB_DATABASE = {
    "Software Engineer - Python": """
    Looking for Python Developer with Django and SQL
    Required Skills: Python, Django, SQL, REST APIs, Git
    """,
    
    "Data Scientist": """
    Hiring Data Scientist with Python and Machine Learning
    Required Skills: Python, pandas, scikit-learn, TensorFlow, SQL
    """,
    
    "Java Backend Developer": """
    Seeking Java Developer with Spring Boot experience
    Required Skills: Java, Spring Boot, Microservices, MySQL
    """,
    
    "Frontend React Developer": """
    Looking for React Developer
    Required Skills: React, JavaScript, HTML5, CSS3
    """,
    
    "DevOps Engineer": """
    Hiring DevOps Engineer
    Required Skills: AWS, Docker, Kubernetes, Jenkins
    """,
    
    "Full Stack Developer": """
    Seeking Full Stack Developer
    Required Skills: Python/Node.js, React, SQL, Git
    """
}

# Page config
st.set_page_config(
    page_title="ResumeMatchNet",
    page_icon="📄",
    layout="wide"
)

def main():
    st.title("📄 ResumeMatchNet")
    st.markdown("### AI-Powered Resume-Job Description Matching System")
    st.markdown("---")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📄 Resume Upload")
        
        # Resume input methods
        resume_option = st.radio(
            "Choose input method:", 
            ["Upload File", "Paste Text", "Use Sample"],
            horizontal=True
        )
        
        resume_text = ""
        
        if resume_option == "Upload File":
            st.markdown("**Supported formats:** PDF, DOCX, TXT")
            uploaded_file = st.file_uploader(
                "Choose your resume file",
                type=['pdf', 'docx', 'txt'],
                help="Upload your resume in PDF, DOCX, or TXT format"
            )
            
            if uploaded_file:
                with st.spinner("Processing file..."):
                    resume_text = FileProcessor.process_uploaded_file(uploaded_file)
                    
                    if resume_text and not resume_text.startswith("Error"):
                        st.success(f"✅ File '{uploaded_file.name}' processed successfully!")
                        
                        # Show preview
                        with st.expander("Preview extracted text"):
                            st.text_area("Extracted Content:", resume_text[:1000], height=200)
                    else:
                        st.error(resume_text)
            else:
                st.info("📁 Please upload a file")
        
        elif resume_option == "Paste Text":
            resume_text = st.text_area(
                "Paste your resume here:",
                height=300,
                placeholder="Copy and paste your resume content here..."
            )
        
        else:  # Use Sample
            sample_resume = """
John Doe - Senior Software Engineer
Email: john.doe@email.com | Phone: (555) 123-4567

SUMMARY
Experienced Software Engineer with 5+ years in Python development.
Strong background in web development and machine learning.

TECHNICAL SKILLS
- Languages: Python, JavaScript, SQL
- Frameworks: Django, Flask, React
- Databases: PostgreSQL, MySQL, MongoDB
- Tools: Git, Docker, AWS
- ML: scikit-learn, pandas, numpy

EXPERIENCE
Senior Software Engineer | Tech Corp (2020-Present)
- Developed REST APIs using Django and Django REST Framework
- Built ML models for customer churn prediction
- Reduced API response time by 40%

Software Developer | Web Solutions (2018-2020)
- Created web applications using Python and Flask
- Implemented database designs with PostgreSQL

EDUCATION
M.S. in Computer Science | University of Technology (2018)
B.S. in Software Engineering | State University (2016)

CERTIFICATIONS
- AWS Certified Developer
- Python Institute PCPP
"""
            if st.button("📋 Load Sample Resume", use_container_width=True):
                resume_text = sample_resume
                st.success("Sample resume loaded!")
            
            if 'resume_text' in locals() and resume_text:
                st.text_area("Sample Resume:", sample_resume, height=250)
    
    with col2:
        st.header("💼 Job Description")
        
        job_option = st.radio(
            "Choose input method:",
            ["Select from Database", "Paste Text", "Upload File"],
            horizontal=True
        )
        
        job_text = ""
        
        if job_option == "Select from Database":
            job_titles = list(JOB_DATABASE.keys())
            selected_job = st.selectbox("Select a job position:", job_titles)
            if selected_job:
                job_text = JOB_DATABASE[selected_job]
                st.success(f"✅ Selected: {selected_job}")
                with st.expander("View Job Description"):
                    st.write(job_text)
        
        elif job_option == "Paste Text":
            job_text = st.text_area(
                "Paste job description here:",
                height=300,
                placeholder="Copy and paste job description here..."
            )
        
        else:  # Upload File for Job
            st.markdown("**Supported formats:** PDF, DOCX, TXT")
            uploaded_job = st.file_uploader(
                "Upload job description file",
                type=['pdf', 'docx', 'txt'],
                key="job_uploader"
            )
            
            if uploaded_job:
                with st.spinner("Processing job description..."):
                    job_text = FileProcessor.process_uploaded_file(uploaded_job)
                    
                    if job_text and not job_text.startswith("Error"):
                        st.success(f"✅ File '{uploaded_job.name}' processed successfully!")
                        with st.expander("Preview extracted text"):
                            st.text_area("Job Description:", job_text[:1000], height=200)
                    else:
                        st.error(job_text)
            else:
                st.info("📁 Upload job description or use other options")
    
    # Match button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        match_button = st.button("🔍 MATCH RESUME WITH JOB", 
                                 use_container_width=True, 
                                 type="primary")
    
    # Perform matching
    if match_button:
        if not resume_text:
            st.error("❌ Please provide a resume (upload, paste, or use sample)")
        elif not job_text:
            st.error("❌ Please provide a job description")
        else:
            with st.spinner("Analyzing and matching..."):
                try:
                    model = ResumeMatchNet()
                    result = model.match(resume_text, job_text)
                    
                    # Display results
                    st.markdown("---")
                    st.header("📊 Matching Results")
                    
                    # Score metrics in columns
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("🎯 Overall Match", f"{result['match_score']}%")
                    with col2:
                        st.metric("🔧 Skills Match", f"{result['skill_match_score']}%")
                    with col3:
                        st.metric("📝 Text Similarity", f"{result['text_similarity']}%")
                    with col4:
                        skill_count = f"{result['skill_count']['matched']}/{result['skill_count']['job']}"
                        st.metric("Skills Matched", skill_count)
                    
                    # Progress bar
                    st.subheader("📈 Match Score Visualization")
                    st.progress(result['match_score'] / 100)
                    
                    # Skills analysis
                    st.subheader("🔧 Skills Analysis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**✅ Matched Skills**")
                        if result['matched_skills']:
                            for skill in sorted(result['matched_skills']):
                                st.markdown(f"- ✓ {skill}")
                        else:
                            st.warning("No matching skills found")
                        
                        st.markdown("---")
                        st.markdown("**📋 Your Resume Skills**")
                        if result['resume_skills']:
                            for skill in sorted(result['resume_skills'])[:15]:
                                st.markdown(f"- {skill}")
                        else:
                            st.info("No skills detected in resume")
                    
                    with col2:
                        st.markdown("**❌ Missing Skills (Required by Job)**")
                        if result['missing_skills']:
                            for skill in sorted(result['missing_skills']):
                                st.markdown(f"- ✗ {skill}")
                        else:
                            st.success("🎉 All required skills matched!")
                        
                        st.markdown("---")
                        st.markdown("**💼 Job Required Skills**")
                        if result['job_skills']:
                            for skill in sorted(result['job_skills']):
                                st.markdown(f"- {skill}")
                        else:
                            st.info("No skills detected in job description")
                    
                    # Recommendation
                    st.subheader("💡 Recommendation")
                    if result['match_score'] >= 70:
                        st.success("🎉 **Excellent Match!** This candidate is highly suitable for the position.")
                    elif result['match_score'] >= 50:
                        st.warning("📈 **Good Match** - Consider highlighting the missing skills in your resume.")
                    else:
                        st.error("⚠️ **Low Match** - Significant gaps detected. Review job requirements and update resume.")
                    
                    # Tips for improvement
                    if result['missing_skills']:
                        st.subheader("📝 Tips to Improve Your Match")
                        for skill in result['missing_skills'][:3]:
                            st.markdown(f"- Add **{skill}** to your skills section if you have experience")
                    
                except Exception as e:
                    st.error(f"Error during matching: {str(e)}")
                    st.info("Please make sure both resume and job description contain meaningful text.")

if __name__ == "__main__":
    main()