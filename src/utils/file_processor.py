# Location: C:\Users\asim2\Desktop\ResumeMatchNet\src\utils\file_processor.py

import re
import PyPDF2
import docx2txt

class FileProcessor:
    """Handle file uploads for resumes"""
    
    @staticmethod
    def extract_text_from_pdf(file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text if text else "No text found in PDF"
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    @staticmethod
    def extract_text_from_docx(file):
        """Extract text from DOCX file"""
        try:
            text = docx2txt.process(file)
            return text if text else "No text found in DOCX"
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    @staticmethod
    def extract_text_from_txt(file):
        """Extract text from TXT file"""
        try:
            text = file.read().decode('utf-8')
            return text if text else "No text found in TXT"
        except Exception as e:
            return f"Error reading TXT: {str(e)}"
    
    @staticmethod
    def process_uploaded_file(uploaded_file):
        """Route file to appropriate parser based on type"""
        if uploaded_file is not None:
            file_type = uploaded_file.type
            
            if file_type == "application/pdf":
                return FileProcessor.extract_text_from_pdf(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return FileProcessor.extract_text_from_docx(uploaded_file)
            elif file_type == "text/plain":
                return FileProcessor.extract_text_from_txt(uploaded_file)
            else:
                return f"Unsupported file type: {file_type}. Please upload PDF, DOCX, or TXT."
        return None