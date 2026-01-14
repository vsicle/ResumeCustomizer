"""
Gemini API integration for tailoring resume content to job descriptions.
"""

import json
import os
import re
from pathlib import Path


DEFAULT_MODEL = 'gemini-2.5-flash-lite'


def load_env_config() -> dict:
    """Load configuration from .env file or environment."""
    config = {
        'api_key': os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY'),
        'model': os.environ.get('GEMINI_MODEL'),
    }
    
    # Try .env file for missing values
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GEMINI_API_KEY=') and not config['api_key']:
                    config['api_key'] = line.split('=', 1)[1]
                elif line.startswith('GEMINI_MODEL=') and not config['model']:
                    config['model'] = line.split('=', 1)[1]
    
    return config


def load_api_key() -> str:
    """Load Gemini API key from .env file or environment."""
    config = load_env_config()
    if config['api_key']:
        return config['api_key']
    raise ValueError("No API key found. Set GEMINI_API_KEY in .env or environment.")


def get_model() -> str:
    """Get the configured model name, or default."""
    config = load_env_config()
    return config['model'] or DEFAULT_MODEL


def extract_all_keywords(master_data: dict) -> list[str]:
    """Extract all unique keywords from master resume to restrict Gemini's output."""
    keywords = set()
    
    # From skills
    for skill_list in master_data.get('skills', {}).values():
        if isinstance(skill_list, list):
            keywords.update(skill_list)
    
    # From work
    for job in master_data.get('work', []):
        keywords.update(job.get('keywords', []))
    
    # From projects
    for project in master_data.get('projects', []):
        keywords.update(project.get('keywords', []))
    
    return sorted(keywords)


def build_prompt(master_data: dict, jd_text: str, user_context: str = "") -> str:
    """Build the prompt for Gemini to tailor the resume."""
    all_keywords = extract_all_keywords(master_data)
    
    context_section = ""
    if user_context.strip():
        context_section = f"""
**ADDITIONAL CONTEXT FROM USER:**
{user_context}

"""
    
    prompt = f"""You are an expert resume writer who creates highly targeted, ATS-optimized resumes. Your goal is to create a FULL one-page resume that maximizes relevance to the job description.

**JOB DESCRIPTION:**
{jd_text}
{context_section}
**MASTER RESUME DATA:**
{json.dumps(master_data, indent=2)}

**ALLOWED KEYWORDS:**
{json.dumps(all_keywords)}

**YOUR TASK:**
Create a targeted resume that fills exactly ONE PAGE. You must balance quantity and quality.

**CONTENT SELECTION (MUST fill the entire page - no whitespace at bottom):**
- Include ALL work experiences that have any relevance
- Include 4-6 projects, prioritized by relevance to the JD
- For each item: include exactly 3-4 bullet points (no more than 4)
- Order all items by relevance (most relevant first)

**TECHNICAL SKILLS TAILORING:**
- NEVER add new skills that are not already in the input resume - only use skills from the master resume data
- REMOVE skills that are irrelevant or low-value for this specific JD (be aggressive about trimming)
- REORDER skills within each category: place skills mentioned in the JD FIRST, then related/transferable skills, then general skills
- You may slightly rephrase skill names to match JD terminology (e.g., "Next.js" → "NextJS" if JD uses that form)
- The goal is a focused, high-signal skills section - quality over quantity

**BULLET POINT REWRITING - WORK EXPERIENCE (be aggressive but truthful):**
- Reframe each bullet to emphasize skills/technologies mentioned in the JD
- Mirror the JD's language and terminology where the experience genuinely applies
- Lead with strong action verbs; quantify results wherever possible
- Maximum 200 characters per bullet
- Remove any [cite: XXX] markers

**BULLET POINT REWRITING - PROJECTS (be aggressive but truthful):**
- REWRITE every project bullet to directly connect to JD requirements
- Emphasize technologies, methodologies, and outcomes that match what the JD is looking for
- Frame personal/academic projects as professional-grade work with impact
- Use JD keywords naturally (e.g., if JD mentions "LLMs", highlight any AI/ML work prominently)
- Show initiative, problem-solving, and shipping ability
- Maximum 200 characters per bullet

**INTEGRITY RULES (never break these):**
- NEVER invent experiences, metrics, or technologies not implied by the original
- NEVER claim proficiency in tools/languages not in the original resume
- NEVER add skills from the JD that are not in the input resume's skills section
- You may reframe HOW something is described, but not WHAT was done
- Keep all dates, company names, and education details exactly as provided
- For "keywords" arrays: ONLY use keywords from the ALLOWED KEYWORDS list

**OUTPUT:**
1. Return ONLY valid JSON - no markdown, no explanations, no code blocks
2. Keep the EXACT same JSON structure as the input
3. Ensure enough content for a full single-page resume"""

    return prompt


def tailor_resume(master_data: dict, jd_text: str, user_context: str = "") -> dict:
    """Call Gemini API to tailor resume content."""
    from google import genai
    
    model_name = get_model()
    print(f"Calling Gemini API ({model_name}) to tailor resume...")
    
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    
    prompt = build_prompt(master_data, jd_text, user_context)
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    
    # Extract the response text
    response_text = response.text.strip()
    
    # Clean up response - remove markdown code blocks if present
    if response_text.startswith('```'):
        # Remove ```json and ``` markers
        response_text = re.sub(r'^```(?:json)?\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
    
    try:
        tailored_data = json.loads(response_text)
        print("Successfully parsed Gemini response.")
        return tailored_data
    except json.JSONDecodeError as e:
        print(f"Failed to parse Gemini response as JSON: {e}")
        print("Raw response:")
        print(response_text[:500])
        raise ValueError("Gemini did not return valid JSON")


def suggest_skills(master_data: dict, jd_text: str) -> list[str]:
    """Call Gemini to suggest skills from JD that aren't in the resume."""
    from google import genai
    
    existing_skills = set()
    for skill_list in master_data.get('skills', {}).values():
        if isinstance(skill_list, list):
            existing_skills.update(s.lower().strip() for s in skill_list)
    
    prompt = f"""Analyze this job description and identify skills/technologies that are mentioned but NOT present in the candidate's resume.

**JOB DESCRIPTION:**
{jd_text}

**CANDIDATE'S CURRENT SKILLS:**
{json.dumps(master_data.get('skills', {}), indent=2)}

**TASK:**
List only skills/technologies from the JD that the candidate does NOT already have listed.
Return a JSON array of strings, e.g., ["Go", "Kubernetes", "GraphQL"]
Only include technical skills, languages, frameworks, or tools - not soft skills.
Return an empty array [] if no new skills are found.
Return ONLY the JSON array - no markdown, no explanation."""

    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model=get_model(),
        contents=prompt,
    )
    
    response_text = response.text.strip()
    if response_text.startswith('```'):
        response_text = re.sub(r'^```(?:json)?\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
    
    try:
        suggestions = json.loads(response_text)
        if isinstance(suggestions, list):
            return [s for s in suggestions if s.lower().strip() not in existing_skills]
        return []
    except json.JSONDecodeError:
        return []


def prompt_for_skills(suggested_skills: list[str]) -> list[str]:
    """Ask user which suggested skills they actually possess."""
    if not suggested_skills:
        return []
    
    print("\n" + "="*60)
    print("SKILL SUGGESTIONS: The JD mentions these skills not in your resume.")
    print("For each, indicate if you have this skill (y/n):")
    print("="*60)
    
    confirmed_skills = []
    for skill in suggested_skills:
        while True:
            response = input(f"  Do you know {skill}? [y/n]: ").strip().lower()
            if response in ('y', 'yes'):
                confirmed_skills.append(skill)
                break
            elif response in ('n', 'no'):
                break
            else:
                print("    Please enter 'y' or 'n'")
    
    if confirmed_skills:
        print(f"\nAdding confirmed skills: {', '.join(confirmed_skills)}")
    else:
        print("\nNo new skills to add.")
    
    return confirmed_skills


def add_skills_to_resume(master_data: dict, new_skills: list[str]) -> dict:
    """Add confirmed skills to the resume data."""
    if not new_skills:
        return master_data
    
    data = json.loads(json.dumps(master_data))  # Deep copy
    
    # Add to tools by default (most flexible category)
    if 'tools' not in data.get('skills', {}):
        data['skills']['tools'] = []
    
    data['skills']['tools'].extend(new_skills)
    return data


def save_temp_resume(data: dict, output_path: Path) -> None:
    """Save tailored resume to temp file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Tailored resume saved to: {output_path}")
