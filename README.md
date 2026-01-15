# Resume Compiler

An AI-powered tool that generates tailored, single-page PDF resumes from a master resume and job description. Uses Google's Gemini API to intelligently select and rewrite content to maximize relevance for each application.

## Features

- **AI-Powered Tailoring**: Automatically rewrites bullet points to match job description terminology
- **Smart Content Selection**: Prioritizes most relevant work experience and projects
- **Skill Suggestions**: Identifies skills from the JD you may have forgotten to include
- **Strict Formatting**: Generates Harvard-format, single-page PDF via LaTeX
- **ATS Optimization**: Reorders and emphasizes keywords for applicant tracking systems

## Prerequisites

- **Python 3.12+**
- **LaTeX Distribution** (for PDF generation)
  - Windows: [MiKTeX](https://miktex.org/download)
  - macOS: `brew install --cask mactex`
  - Linux: `sudo apt install texlive-full`
- **Gemini API Key**: Get one free at [Google AI Studio](https://aistudio.google.com/apikey)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vsicle/ResumeCustomizer.git
   cd ResumeCustomizer
   ```

2. **Install Python dependencies**
   ```bash
   pip install jinja2 google-genai
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Setup Your Resume Data

### 1. Edit Master Resume (`data/master_resume.json`)

This is your complete experience pool. Include everything—the AI will select what's relevant.

```json
{
  "basics": {
    "name": "YOUR NAME",
    "email": "your.email@example.com",
    "phone": "(555) 123-4567",
    "website": "yourwebsite.com",
    "github": "github.com/yourusername",
    "location": "City, State",
    "education": {
      "institution": "University Name",
      "area": "Degree Program",
      "endDate": "Expected May 2026",
      "score": "GPA: X.X/4.0"
    }
  },
  "skills": {
    "languages": ["Python", "JavaScript", "..."],
    "frameworks": [".NET", "React", "..."],
    "tools": ["Git", "Docker", "..."],
    "concepts": ["REST APIs", "CI/CD", "..."]
  },
  "work": [
    {
      "name": "Company Name",
      "position": "Job Title",
      "startDate": "Month Year",
      "endDate": "Present",
      "highlights": [
        "Accomplishment with metrics...",
        "Another accomplishment..."
      ],
      "keywords": ["Python", "AWS", "..."]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "startDate": "2024",
      "endDate": "2024",
      "highlights": [
        "What you built and the impact...",
        "Technologies used and outcomes..."
      ],
      "keywords": ["React", "Node.js", "..."]
    }
  ]
}
```

### 2. Add Job Description (`data/job_description.txt`)

Paste the full job posting text. Include:
- Job title and company
- Responsibilities
- Requirements
- Preferred qualifications

## Usage

### Interactive Mode (Recommended)
```bash
python src/builder.py
```

The tool will:
1. Suggest skills from the JD you might have (confirm y/n for each)
2. Ask for optional context (e.g., "emphasize backend experience")
3. Generate tailored resume to `data/temp_resume.json`
4. Ask for approval before generating PDF
5. Output final PDF to `output/resume.pdf`

### With Context Flag
```bash
python src/builder.py -c "focus on AI/ML and distributed systems"
```

### Auto Mode (No Prompts)
```bash
python src/builder.py -y
```

### Skip AI Tailoring
```bash
python src/builder.py --no-tailor
```

### Quick Build (Paste JSON)
For quick PDF generation without AI tailoring or JD matching:
1. Paste your resume JSON into `data/paste_resume.json`
2. Run `python src/quick_build.py`
3. Output: `output/resume.pdf`

### VS Code
Use the included launch configurations in `.vscode/launch.json`:
- **Quick Build (paste JSON)** - Paste JSON, get PDF (no AI, no JD)
- **Build Resume (with AI)** - Full interactive mode


## Output

- `data/temp_resume.json` - Tailored JSON (review before PDF generation)
- `output/resume.pdf` - Final formatted PDF

## File Structure

```
ResumeCustomizer/
├── data/
│   ├── master_resume.json    # Your complete experience (EDIT THIS)
│   ├── job_description.txt   # Target job posting (REPLACE PER APPLICATION)
│   └── temp_resume.json      # Generated tailored version
├── src/
│   ├── builder.py            # Main entry point
│   ├── tailor.py             # Gemini API integration
│   └── scorer.py             # Content selection logic
├── templates/
│   └── resume.tex            # LaTeX template
├── output/
│   └── resume.pdf            # Generated PDF
├── .env.example              # Environment template
└── .env                      # Your API keys (create from .env.example)
```

## Customization

### Modify LaTeX Template
Edit `templates/resume.tex` to change formatting, fonts, or layout.

### Adjust AI Behavior
Edit prompts in `src/tailor.py`:
- `build_prompt()` - Main tailoring instructions
- `suggest_skills()` - Skill suggestion logic
- `temperature` - Controls output consistency (default: 0.3, lower = more deterministic)

### Change Gemini Model
Set `GEMINI_MODEL` in `.env`:
```
GEMINI_MODEL=gemini-2.5-flash      # Default, good balance
GEMINI_MODEL=gemini-2.5-pro        # Higher quality, slower
GEMINI_MODEL=gemini-2.5-flash-lite # Fastest, less consistent
```

## Troubleshooting

**"pdflatex not found"**  
Install a LaTeX distribution (see Prerequisites).

**"No API key found"**  
Ensure `.env` exists with `GEMINI_API_KEY=your_key`.

**Resume exceeds one page**  
The AI aims for exactly one page. If overflow occurs, reduce content in `master_resume.json` or adjust the LaTeX template margins.
