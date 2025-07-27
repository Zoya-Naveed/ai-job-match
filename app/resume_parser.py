import re

def extract_skills(resume_text):
    known_skills = [
        "python", "java", "sql", "machine learning", "data analysis", "fastapi", "django",
        "javascript", "html", "css", "project management", "communication", "teamwork",
        "git", "react", "node.js", "docker", "rest apis", "linux", "pandas", "azure"
    ]

    resume_text = resume_text.lower()
    
    extracted = []
    for skill in known_skills:
        # Escape special regex characters in skill string (like '.' in node.js)
        escaped_skill = re.escape(skill)
        # Use word boundaries for single words, and allow spaces for multi-word skills
        if " " in skill:
            # For multi-word skills like 'rest apis', just do a simple substring search
            if skill in resume_text:
                extracted.append(skill)
        else:
            # For single word skills, use word boundary regex to avoid partial matches
            pattern = r'\b' + escaped_skill + r'\b'
            if re.search(pattern, resume_text):
                extracted.append(skill)

    print("DEBUG: Extracted skills:", extracted)  # Debug output for your logs
    return extracted
