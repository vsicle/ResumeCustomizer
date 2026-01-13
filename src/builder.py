"""
Main builder script for generating tailored resumes.
"""

import json
import subprocess
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from scorer import select_content


# Space budget constants
TOTAL_LINES = 55
FIXED_COST = 10  # Header + Education + Skills
WORK_LIMIT = 35
PROJECTS_LIMIT = 50


def estimate_lines(item: dict) -> int:
    """Estimate the number of lines an item will consume."""
    header_lines = 2  # Title line + company/tech line
    bullet_lines = len(item.get('highlights', item.get('bullets', [])))
    return header_lines + bullet_lines


def apply_space_budget(
    sorted_work: list[dict],
    sorted_projects: list[dict],
    achievements: list[dict] | None = None
) -> dict:
    """
    Select items that fit within the page space budget.
    
    Returns selected_work, selected_projects, and optionally selected_achievements.
    """
    lines_used = FIXED_COST
    selected_work = []
    selected_projects = []
    selected_achievements = []
    
    # Add work items until we hit WORK_LIMIT
    for item in sorted_work:
        item_lines = estimate_lines(item)
        if lines_used + item_lines <= WORK_LIMIT:
            selected_work.append(item)
            lines_used += item_lines
    
    # Add project items until we hit PROJECTS_LIMIT
    for item in sorted_projects:
        item_lines = estimate_lines(item)
        if lines_used + item_lines <= PROJECTS_LIMIT:
            selected_projects.append(item)
            lines_used += item_lines
    
    # Add achievements if space remains
    if achievements:
        for item in achievements:
            item_lines = estimate_lines(item)
            if lines_used + item_lines <= TOTAL_LINES:
                selected_achievements.append(item)
                lines_used += item_lines
    
    return {
        'selected_work': selected_work,
        'selected_projects': selected_projects,
        'selected_achievements': selected_achievements,
        'lines_used': lines_used
    }


def escape_latex(text: str) -> str:
    """Escape LaTeX special characters."""
    if not isinstance(text, str):
        return text
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
    ]
    for char, replacement in replacements:
        text = text.replace(char, replacement)
    return text


def create_jinja_env(template_dir: Path) -> Environment:
    """Create Jinja2 environment with LaTeX-compatible delimiters."""
    env = Environment(
        loader=FileSystemLoader(template_dir),
        block_start_string=r'\BLOCK{',
        block_end_string='}',
        variable_start_string=r'\VAR{',
        variable_end_string='}',
        comment_start_string=r'\#{',
        comment_end_string='}',
        line_statement_prefix=None,
        line_comment_prefix=None,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False
    )
    env.filters['e'] = escape_latex
    env.filters['escape_latex'] = escape_latex
    return env


def build_resume(master_path: Path, jd_path: Path, output_dir: Path) -> Path:
    """
    Build a tailored resume PDF.
    
    Args:
        master_path: Path to master_resume.json
        jd_path: Path to job_description.txt
        output_dir: Directory for output files
    
    Returns:
        Path to the generated PDF
    """
    # Load data
    with open(master_path, 'r', encoding='utf-8') as f:
        master_data = json.load(f)
    
    with open(jd_path, 'r', encoding='utf-8') as f:
        jd_text = f.read()
    
    # Score and rank content
    ranked = select_content(master_data, jd_text)
    
    # Apply space budget
    budgeted = apply_space_budget(
        ranked['sorted_work'],
        ranked['sorted_projects'],
        master_data.get('achievements', [])
    )
    
    print(f"Selected {len(budgeted['selected_work'])} work items")
    print(f"Selected {len(budgeted['selected_projects'])} projects")
    print(f"Estimated lines used: {budgeted['lines_used']}/{TOTAL_LINES}")
    
    # Set up Jinja2
    template_dir = Path(__file__).parent.parent / 'templates'
    env = create_jinja_env(template_dir)
    template = env.get_template('resume_master.tex')
    
    # Prepare template context
    context = {
        'basics': master_data.get('basics', {}),
        'skills': master_data.get('skills', {}),
        'selected_work': budgeted['selected_work'],
        'selected_projects': budgeted['selected_projects'],
        'selected_achievements': budgeted['selected_achievements']
    }
    
    # Render template
    rendered = template.render(**context)
    
    # Save output
    output_dir.mkdir(parents=True, exist_ok=True)
    tex_path = output_dir / 'resume.tex'
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(rendered)
    
    print(f"Rendered LaTeX saved to: {tex_path}")
    
    # Run pdflatex
    pdflatex_path = r'C:\Users\Vasko\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe'
    try:
        result = subprocess.run(
            [pdflatex_path, '-interaction=nonstopmode', '-output-directory', str(output_dir), str(tex_path)],
            capture_output=True,
            text=True,
            check=True
        )
        pdf_path = output_dir / 'resume.pdf'
        print(f"PDF generated: {pdf_path}")
        return pdf_path
    except subprocess.CalledProcessError as e:
        print(f"pdflatex failed:\n{e.stdout}\n{e.stderr}", file=sys.stderr)
        raise
    except FileNotFoundError:
        print("pdflatex not found. Please install a LaTeX distribution.", file=sys.stderr)
        raise


def main():
    """Main entry point."""
    root = Path(__file__).parent.parent
    
    master_path = root / 'data' / 'master_resume.json'
    jd_path = root / 'data' / 'job_description.txt'
    output_dir = root / 'output'
    
    if not master_path.exists():
        print(f"Error: {master_path} not found", file=sys.stderr)
        sys.exit(1)
    
    if not jd_path.exists():
        print(f"Error: {jd_path} not found", file=sys.stderr)
        sys.exit(1)
    
    build_resume(master_path, jd_path, output_dir)


if __name__ == '__main__':
    main()
