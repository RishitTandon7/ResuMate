import re

def score_ats(text):
    """
    Simple ATS compatibility scoring based on presence of keywords and structure.
    """
    keywords = ['experience', 'education', 'skills', 'projects', 'certifications', 'summary', 'contact']
    score = 0
    text_lower = text.lower()
    for keyword in keywords:
        if keyword in text_lower:
            score += 10
    # Cap score at 60
    return min(score, 60)

def score_grammar(text):
    """
    Dummy grammar scoring based on counting common grammar mistakes.
    """
    common_mistakes = [' there ', ' their ', ' they\'re ', ' your ', ' you\'re ']
    mistakes_count = 0
    text_lower = text.lower()
    for mistake in common_mistakes:
        mistakes_count += text_lower.count(mistake)
    # Simple scoring: fewer mistakes means higher score
    score = max(0, 40 - mistakes_count * 5)
    return score

def score_format(text):
    """
    Simple format scoring based on presence of bullet points and section headers.
    """
    bullet_points = re.findall(r'[\u2022\-\*]', text)
    section_headers = ['experience', 'education', 'skills', 'projects', 'certifications', 'summary', 'contact']
    score = 0
    if len(bullet_points) > 5:
        score += 15
    text_lower = text.lower()
    for header in section_headers:
        if header in text_lower:
            score += 15
            break
    # Cap score at 30
    return min(score, 30)

def score_resume(text):
    """
    Aggregate scoring function returning a dictionary with ATS, grammar, format, raw scores and total score normalized to 100.
    """
    ats_score = score_ats(text)
    grammar_score = score_grammar(text)
    format_score = score_format(text)
    total_score_raw = ats_score + grammar_score + format_score
    # Normalize scores to 100 total
    ats_norm = round((ats_score / 130) * 100, 2)
    grammar_norm = round((grammar_score / 130) * 100, 2)
    format_norm = round((format_score / 130) * 100, 2)
    total_norm = round(ats_norm + grammar_norm + format_norm, 2)
    return {
        'ats': ats_norm,
        'grammar': grammar_norm,
        'format': format_norm,
        'total': total_norm,
        'ats_raw': ats_score,
        'grammar_raw': grammar_score,
        'format_raw': format_score,
        'total_raw': total_score_raw
    }

