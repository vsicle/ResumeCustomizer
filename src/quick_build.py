"""
Quick build script: paste JSON resume data, get PDF output.
Reads from data/paste_resume.json and generates output/resume.pdf.
"""

import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from builder import render_pdf


def main():
    root = Path(__file__).parent.parent
    paste_path = root / 'data' / 'paste_resume.json'
    output_dir = root / 'output'
    
    if not paste_path.exists():
        print(f"Error: {paste_path} not found", file=sys.stderr)
        print("Paste your JSON into data/paste_resume.json and run again.")
        sys.exit(1)
    
    # Load pasted JSON
    try:
        with open(paste_path, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {paste_path}: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Render PDF with empty JD (no keyword matching)
    print("Generating PDF from pasted JSON...")
    render_pdf(resume_data, "", output_dir)
    print("Done! Output: output/resume.pdf")


if __name__ == '__main__':
    main()
