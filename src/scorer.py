"""
Scorer module for ranking resume content based on job description relevance.
"""

import re
from typing import Any


def extract_keywords(text: str) -> set[str]:
    """Extract keywords from text by splitting and lowercasing."""
    # Remove punctuation and split by whitespace
    words = re.findall(r'\b[a-zA-Z0-9+#]+\b', text.lower())
    # Filter out common stop words
    stop_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
        'we', 'you', 'your', 'our', 'their', 'this', 'that', 'these', 'those'
    }
    return {w for w in words if w not in stop_words and len(w) > 1}


def score_item(item: dict[str, Any], jd_keywords: set[str]) -> float:
    """
    Calculate relevance score for a work/project item.
    
    Scoring factors:
    - Tag matches (weighted higher)
    - Bullet text keyword matches
    """
    score = 0.0
    
    # Score from keywords/tags (high weight)
    keywords = {t.lower() for t in item.get('keywords', item.get('tags', []))}
    keyword_matches = keywords & jd_keywords
    score += len(keyword_matches) * 3.0
    
    # Score from highlights/bullets text
    bullets = item.get('highlights', item.get('bullets', []))
    bullet_text = ' '.join(bullets).lower()
    bullet_keywords = extract_keywords(bullet_text)
    bullet_matches = bullet_keywords & jd_keywords
    score += len(bullet_matches) * 1.0
    
    # Score from tech_stack (for projects)
    tech_stack = {t.lower() for t in item.get('tech_stack', [])}
    tech_matches = tech_stack & jd_keywords
    score += len(tech_matches) * 2.0
    
    return score


def select_content(master_data: dict[str, Any], jd_text: str) -> dict[str, list]:
    """
    Score and sort work experience and projects based on JD relevance.
    
    Args:
        master_data: The master resume data containing 'work' and 'projects'.
        jd_text: The job description text.
    
    Returns:
        Dictionary with 'sorted_work' and 'sorted_projects' lists,
        each sorted by relevance score (descending).
    """
    jd_keywords = extract_keywords(jd_text)
    
    # Score and sort work experience
    work_items = master_data.get('work', [])
    scored_work = [
        (item, score_item(item, jd_keywords))
        for item in work_items
    ]
    sorted_work = [item for item, _ in sorted(scored_work, key=lambda x: x[1], reverse=True)]
    
    # Score and sort projects
    project_items = master_data.get('projects', [])
    scored_projects = [
        (item, score_item(item, jd_keywords))
        for item in project_items
    ]
    sorted_projects = [item for item, _ in sorted(scored_projects, key=lambda x: x[1], reverse=True)]
    
    return {
        'sorted_work': sorted_work,
        'sorted_projects': sorted_projects
    }
