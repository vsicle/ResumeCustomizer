# ChatGPT Resume Tailoring Prompt

Copy this prompt, replace the placeholders, and paste into ChatGPT.

---

## The Prompt

```
I need you to rewrite my resume bullet points to be tailored for a specific job. 

**Output Format:** Return ONLY valid JSON that I can paste directly into my resume system. No explanations, no markdown code blocks, just raw JSON.

**Job Description:**
[PASTE JOB DESCRIPTION HERE]

**My Current Experience:**
[PASTE YOUR WORK/PROJECT JSON HERE]

**Instructions:**
1. Rewrite each "highlights" bullet to:
   - Use keywords from the job description naturally
   - Start with strong action verbs
   - Include metrics/numbers where possible
   - Keep each bullet under 200 characters
   - Remove citation markers like [cite: XXX]

2. Update the "keywords" array to match job requirements

3. Keep the same JSON structure exactly

4. Return the complete JSON array for work OR projects (whichever I provided)

**Example output format for work:**
[
  {
    "name": "Company Name",
    "position": "Job Title",
    "startDate": "Month Year",
    "endDate": "Present",
    "highlights": [
      "Rewritten bullet 1",
      "Rewritten bullet 2"
    ],
    "keywords": ["Keyword1", "Keyword2"]
  }
]
```

---

## Quick Workflow

1. **Copy** the job description into `data/job_description.txt`

2. **Ask ChatGPT** to tailor your work experience:
   ```
   [Paste the prompt above]
   
   Job Description:
   [Paste JD]
   
   My Current Experience:
   [Copy-paste the "work" array from master_resume.json]
   ```

3. **Replace** the `"work": [...]` section in `master_resume.json` with ChatGPT's output

4. **Repeat** for projects if needed

5. **Run** `python src/builder.py`

---

## One-Shot Full Resume Prompt

For a complete tailored resume in one go:

```
Rewrite my resume content to match this job description. Return ONLY valid JSON.

**Job Description:**
[PASTE JD]

**My Resume Data:**
[PASTE ENTIRE master_resume.json]

**Rules:**
- Keep exact JSON structure
- Rewrite all highlights to use JD keywords naturally
- Update all keywords arrays to match JD requirements  
- Remove [cite: XXX] markers
- Keep bullets concise (<200 chars)
- Do NOT change: name, dates, company names, school info
- Return the complete JSON object
```

---

## Tips

- **Verify JSON validity** before pasting: Use [jsonlint.com](https://jsonlint.com)
- **Keep originals**: Backup `master_resume.json` before replacing
- **Iterate**: Ask ChatGPT to "make bullet 2 more technical" if needed
