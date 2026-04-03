# Location: C:\Users\asim2\Desktop\ResumeMatchNet\src\data\processor.py

import re

class FileProcessor:
    @staticmethod
    def extract_text_from_pdf(file):
        """Extract text from PDF (simplified)"""
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except:
            return "Error reading PDF"
    
    @staticmethod
    def extract_text_from_docx(file):
        """Extract text from DOCX (simplified)"""
        try:
            import docx2txt
            return docx2txt.process(file)
        except:
            return "Error reading DOCX"
    
    @staticmethod
    def extract_text_from_txt(file):
        """Extract text from TXT"""
        try:
            return file.read().decode('utf-8')
        except:
            return "Error reading TXT"
        