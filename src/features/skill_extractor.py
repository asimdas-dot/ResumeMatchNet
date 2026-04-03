class SkillExtractor:
    SKILL_DB = {
        'python', 'java', 'sql', 'aws', 'docker', 'kubernetes'
    }
    
    def extract_skills(self, text):
        """Extract skills from text"""
        found = set()
        for skill in self.SKILL_DB:
            if skill in text.lower():
                found.add(skill)
        return found