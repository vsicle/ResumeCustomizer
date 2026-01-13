# Resume Compiler - Usage Guide

## Quick Start

1. **Edit your master resume data** in `data/master_resume.json`
2. **Paste the job description** into `data/job_description.txt`
3. **Run the builder**:
   ```bash
   build.bat
   ```
   Or directly:
   ```bash
   python src/builder.py
   ```
4. **Review** the tailored content when prompted
5. **Find your resume** at `output/resume.pdf`

---

## Commands

| Command | Description |
|---------|-------------|
| `build.bat` | Run with AI tailoring (default) |
| `build.bat --no-tailor` | Skip AI, use master_resume.json directly |
| `build.bat -y` | Skip approval prompt, generate PDF immediately |
| `build.bat --no-tailor -y` | Fast mode: no AI, no prompts |

---

## AI Tailoring (Gemini)

By default, the builder calls Gemini API to tailor your resume content:

1. Rewrites bullet points to match job description keywords
2. Makes slight adjustments to position titles
3. Only uses keywords already in your master_resume.json (no fabrication)
4. Saves tailored content to `data/temp_resume.json` for review

### Setup

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```

### Install Dependencies

```bash
pip install google-genai jinja2
```

---

## File Structure

```
ResumeCustomizer/
├── data/
│   ├── master_resume.json    # Your complete resume data
│   └── job_description.txt   # Target job description
├── src/
│   ├── builder.py            # Main script
│   └── scorer.py             # Content ranking logic
├── templates/
│   └── resume_master.tex     # LaTeX template
└── output/
    ├── resume.tex            # Generated LaTeX
    └── resume.pdf            # Final PDF
```

---

## How It Works

1. **Keyword Extraction**: Extracts keywords from the job description
2. **Content Scoring**: Ranks your work experience and projects by relevance
3. **Space Budget**: Selects items that fit on a single page (~55 lines)
4. **PDF Generation**: Renders LaTeX template and compiles with pdflatex

---

## Customizing Your Resume

### Edit `data/master_resume.json`

```json
{
  "basics": {
    "name": "Your Name",
    "email": "email@example.com",
    "phone": "(123) 456-7890",
    "website": "yourwebsite.com",
    "github": "github.com/username",
    "location": "City, ST",
    "education": { ... }
  },
  "skills": {
    "languages": ["Python", "JavaScript", ...],
    "frameworks": [".NET", "React", ...],
    "tools": ["Docker", "AWS", ...],
    "concepts": ["REST APIs", "CI/CD", ...]
  },
  "work": [
    {
      "name": "Company Name",
      "position": "Job Title",
      "startDate": "Month Year",
      "endDate": "Present",
      "highlights": ["Achievement 1", "Achievement 2"],
      "keywords": ["Python", "AWS", "Networking"]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "startDate": "Year",
      "endDate": "Year",
      "highlights": ["What you built", "Technologies used"],
      "keywords": ["Rust", "Security", "API"]
    }
  ]
}
```

### Keywords Matter

The `keywords` array in each work/project entry is used for matching against the job description. Add relevant technologies, concepts, and skills to improve ranking.

---

## Requirements

- **Python 3.10+**
- **Jinja2**: `pip install jinja2`
- **MiKTeX** or **TeX Live** (for pdflatex)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `pdflatex not found` | Install MiKTeX or add it to PATH |
| Resume is 2+ pages | Reduce bullet points or adjust space budget in `builder.py` |
| Special characters break PDF | They're auto-escaped; check for unusual Unicode |
