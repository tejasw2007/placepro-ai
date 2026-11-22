import re

def extract_tokens(text):
    if not text:
        return set()
    parts = re.split(r'[,;\n|/]+', text.lower())
    tokens = set()
    for part in parts:
        cleaned = part.strip()
        if cleaned:
            tokens.add(cleaned)
            for word in re.findall(r'[a-z0-9\+\#\.]{2,}', cleaned):
                tokens.add(word)
    return tokens

def calculate_resume_match(student_skills, resume_summary, job_required_skills):
    req_list = [s.strip().lower() for s in (job_required_skills or '').split(',') if s.strip()]
    if not req_list:
        return {"match_score": 100.0, "matched": [], "missing": []}

    candidate_tokens = extract_tokens(student_skills).union(extract_tokens(resume_summary))
    matched = []
    missing = []

    for req in req_list:
        req_words = set(re.findall(r'[a-z0-9\+\#\.]{2,}', req))
        if req in candidate_tokens or (req_words and req_words.issubset(candidate_tokens)):
            matched.append(req.title())
        else:
            missing.append(req.title())

    score = round((len(matched) / len(req_list)) * 100, 1)
    return {
        "match_score": score,
        "matched": matched,
        "missing": missing
    }

def calculate_readiness_score(cgpa, skills, resume_summary=''):
    try:
        cgpa_val = max(0.0, min(10.0, float(cgpa or 0.0)))
    except (TypeError, ValueError):
        cgpa_val = 0.0

    cgpa_component = (cgpa_val / 10.0) * 40.0
    skill_list = [s.strip() for s in (skills or '').split(',') if s.strip()]
    summary_bonus = 10.0 if len((resume_summary or '').strip()) >= 40 else 0.0
    skill_component = min(50.0, len(skill_list) * 7.5) + summary_bonus

    return round(min(100.0, cgpa_component + skill_component), 1)