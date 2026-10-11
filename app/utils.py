import re

# Comprehensive list of standard tech & analytics keywords for normalization
TECH_KEYWORDS = {
    'python', 'sql', 'mysql', 'postgresql', 'sqlite', 'data analysis', 'data analyst',
    'excel', 'vba', 'pandas', 'numpy', 'machine learning', 'artificial intelligence', 'ai',
    'flask', 'django', 'html', 'css', 'javascript', 'git', 'github', 'power bi', 'tableau',
    'rest api', 'deep learning', 'cloud', 'aws', 'docker', 'statistics', 'problem solving'
}

def extract_keywords(text: str) -> set:
    """Extracts, cleans, and matches standard keywords from free text."""
    if not text:
        return set()
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    found_keywords = set()
    for kw in TECH_KEYWORDS:
        if kw in cleaned:
            found_keywords.add(kw)
    
    # Also parse direct comma-separated tokens
    tokens = [t.strip().lower() for t in text.split(',') if t.strip()]
    for token in tokens:
        if len(token) > 1:
            found_keywords.add(token)
            
    return found_keywords

def calculate_resume_match(student_skills: str, student_summary: str, job_skills: str) -> dict:
    """
    Analyzes student skills & resume summary against job requirements.
    Returns matching score, matched keywords, and missing keywords.
    """
    combined_student_text = f"{student_skills} {student_summary}"
    student_tokens = extract_keywords(combined_student_text)
    required_tokens = extract_keywords(job_skills)

    if not required_tokens:
        return {"match_score": 100.0, "matched": [], "missing": []}

    matched = student_tokens.intersection(required_tokens)
    missing = required_tokens - student_tokens

    match_percentage = round((len(matched) / len(required_tokens)) * 100, 1)

    return {
        "match_score": min(match_percentage, 100.0),
        "matched": sorted(list(matched)),
        "missing": sorted(list(missing))
    }

def calculate_readiness_score(cgpa: float, skills_str: str, summary_str: str) -> float:
    """
    Computes a 0-100 Placement Readiness index:
    - CGPA weight: 40% (Normalized on scale of 10)
    - Skills & Summary density weight: 60%
    """
    cgpa_component = (min(max(cgpa, 0.0), 10.0) / 10.0) * 40.0
    
    extracted = extract_keywords(f"{skills_str} {summary_str}")
    skill_count = len(extracted)
    
    # Having 8+ distinct technical skills yields full skill points
    skill_component = min(skill_count / 8.0, 1.0) * 60.0

    return round(cgpa_component + skill_component, 1)