# Resume Compiler - Usage Guide

## Quick Start

1. **Edit your master resume data** in `data/master_resume.json`
2. **Paste the job description** into `data/job_description.txt`
3. **Run the builder**:
   ```bash
   python src/builder.py
   ```
4. **Find your resume** at `output/resume.pdf`

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
