"""
Resume PDF Parser for Abhijeet V S Portfolio
Extracts structured information from PDF resumes and updates MySQL database.
"""

import re
import json
import logging
from pathlib import Path

try:
    import pdfplumber
    PDF_PLUMBER_AVAILABLE = True
except ImportError:
    PDF_PLUMBER_AVAILABLE = False

try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

logger = logging.getLogger(__name__)


# ── Section keyword maps ──────────────────────────────────────────────────────
SECTION_PATTERNS = {
    'summary': r'(professional\s+summary|summary|objective|profile|about)',
    'education': r'(education|academic|qualification)',
    'skills': r'(skills|technical\s+skills|competencies|expertise)',
    'projects': r'(projects|work\s+done|portfolio)',
    'certifications': r'(certifications?|certificates?|courses?)',
    'achievements': r'(achievements?|accomplishments?|awards?|honors?)',
    'contact': r'(contact|personal\s+info|personal\s+details)',
    'experience': r'(experience|work\s+experience|employment)',
}

SKILL_CATEGORIES = {
    'Programming': ['python', 'java', 'c', 'c++', 'javascript', 'typescript', 'arduino', 'kotlin', 'swift', 'go', 'rust', 'php', 'ruby', 'scala'],
    'Web': ['html', 'css', 'react', 'angular', 'vue', 'flask', 'django', 'node', 'express', 'bootstrap', 'tailwind'],
    'Databases': ['mysql', 'mongodb', 'postgresql', 'sqlite', 'redis', 'firebase', 'dynamodb'],
    'AI & Analytics': ['machine learning', 'deep learning', 'data analysis', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit', 'data storytelling', 'risk profiling', 'anomaly detection', 'predictive analytics'],
    'Technologies': ['iot', 'embedded', 'ble', 'bluetooth', 'arduino', 'esp32', 'raspberry pi', 'mqtt', 'docker', 'kubernetes', 'aws', 'azure', 'git', 'linux'],
}


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract raw text from PDF using pdfplumber with pypdf fallback."""
    text = ""

    if PDF_PLUMBER_AVAILABLE:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
        except Exception as e:
            logger.warning(f"pdfplumber failed: {e}, trying pypdf")

    if PYPDF_AVAILABLE:
        try:
            reader = pypdf.PdfReader(pdf_path)
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
        except Exception as e:
            logger.error(f"pypdf also failed: {e}")

    return text


def split_into_sections(text: str) -> dict:
    """Split resume text into named sections."""
    sections = {}
    lines = text.split('\n')
    current_section = 'header'
    section_content = []
    
    for line in lines:
        line_lower = line.strip().lower()
        matched_section = None
        
        for section_name, pattern in SECTION_PATTERNS.items():
            if re.search(pattern, line_lower) and len(line.strip()) < 60:
                matched_section = section_name
                break
        
        if matched_section:
            sections[current_section] = '\n'.join(section_content)
            current_section = matched_section
            section_content = []
        else:
            section_content.append(line)
    
    sections[current_section] = '\n'.join(section_content)
    return sections


def extract_contact_info(text: str) -> dict:
    """Extract name, email, phone, LinkedIn, GitHub from text."""
    contact = {}
    
    # Email
    email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', text)
    if email_match:
        contact['email'] = email_match.group()
    
    # Phone
    phone_match = re.search(r'(\+?\d[\d\s\-().]{8,14}\d)', text)
    if phone_match:
        contact['phone'] = phone_match.group().strip()
    
    # LinkedIn
    linkedin_match = re.search(r'linkedin\.com/in/[\w\-]+', text, re.IGNORECASE)
    if linkedin_match:
        contact['linkedin'] = 'https://' + linkedin_match.group()
    
    # GitHub
    github_match = re.search(r'github\.com/[\w\-]+', text, re.IGNORECASE)
    if github_match:
        contact['github'] = 'https://' + github_match.group()
    
    # Name (first non-empty line that looks like a name)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:5]:
        if re.match(r'^[A-Za-z][\w\s]{3,50}$', line) and '@' not in line:
            contact['name'] = line
            break
    
    return contact


def extract_skills(skills_text: str) -> list:
    """Extract and categorize skills."""
    found_skills = []
    text_lower = skills_text.lower()
    
    for category, skill_list in SKILL_CATEGORIES.items():
        for skill in skill_list:
            if skill in text_lower:
                # Get proper case from original text
                match = re.search(skill, text_lower)
                if match:
                    start = match.start()
                    end = match.end()
                    proper_name = skills_text[start:end]
                    found_skills.append({
                        'name': proper_name.strip().title(),
                        'category': category,
                        'proficiency': 80
                    })
    
    # Also grab comma/bullet separated skills
    skill_tokens = re.split(r'[,•|·\n\t]+', skills_text)
    for token in skill_tokens:
        token = token.strip()
        if 2 < len(token) < 50 and not any(s['name'].lower() == token.lower() for s in found_skills):
            category = categorize_skill(token)
            found_skills.append({
                'name': token,
                'category': category,
                'proficiency': 75
            })
    
    return found_skills


def categorize_skill(skill: str) -> str:
    """Assign a category to a skill string."""
    skill_lower = skill.lower()
    for category, skill_list in SKILL_CATEGORIES.items():
        if any(s in skill_lower for s in skill_list):
            return category
    return 'Technologies'


def extract_education(edu_text: str) -> list:
    """Extract education entries."""
    education = []
    
    # Look for degree patterns
    degree_patterns = [
        r'(Bachelor|Master|B\.E|B\.Tech|M\.Tech|B\.Sc|M\.Sc|PhD|B\.Com)[^\n]*',
        r'(Engineering|Science|Arts|Commerce)[^\n]*'
    ]
    
    for pattern in degree_patterns:
        matches = re.finditer(pattern, edu_text, re.IGNORECASE)
        for match in matches:
            entry = {'degree': match.group().strip(), 'institution': '', 'cgpa': ''}
            
            # Look for CGPA near the degree
            cgpa_match = re.search(r'(CGPA|GPA|Grade)[:\s]+(\d+\.?\d*)', edu_text[match.start():match.start()+300], re.IGNORECASE)
            if cgpa_match:
                entry['cgpa'] = cgpa_match.group(2)
            
            # Year pattern
            year_match = re.search(r'(20\d{2})', edu_text[match.start():match.start()+200])
            if year_match:
                entry['start_year'] = int(year_match.group())
            
            education.append(entry)
    
    return education


def extract_projects(projects_text: str) -> list:
    """Extract project entries from resume text."""
    projects = []
    
    # Split on common project separators
    project_blocks = re.split(r'\n(?=[A-Z][^\n]{5,80}\n)', projects_text)
    
    for block in project_blocks:
        if len(block.strip()) < 20:
            continue
        
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if not lines:
            continue
        
        title = lines[0]
        description = ' '.join(lines[1:4]) if len(lines) > 1 else ''
        
        # Extract technologies
        tech_match = re.search(r'(Technologies?|Tech Stack|Tools?)[:\s]+([^\n]+)', block, re.IGNORECASE)
        technologies = tech_match.group(2).strip() if tech_match else ''
        
        # Bullet points as features
        features = [l.lstrip('•-* ') for l in lines if l.startswith(('•', '-', '*', '–'))]
        
        if len(title) > 5:
            projects.append({
                'title': title,
                'description': description,
                'technologies': technologies,
                'features': '\n'.join(features),
            })
    
    return projects


def extract_certifications(cert_text: str) -> list:
    """Extract certification entries."""
    certs = []
    lines = [l.strip() for l in cert_text.split('\n') if l.strip()]
    
    for line in lines:
        # Skip short or decorative lines
        if len(line) < 10 or re.match(r'^[-=*•]+$', line):
            continue
        
        # Try to extract issuer (usually after dash or comma)
        issuer_match = re.search(r'[-–]\s*([A-Z][^\n,]+)$', line)
        issuer = issuer_match.group(1).strip() if issuer_match else 'Unknown'
        
        name = re.sub(r'\s*[-–][^-]*$', '', line).strip()
        
        if len(name) > 8:
            certs.append({'name': name, 'issuer': issuer})
    
    return certs


def extract_achievements(ach_text: str) -> list:
    """Extract achievement entries."""
    achievements = []
    lines = [l.strip() for l in ach_text.split('\n') if l.strip()]
    
    for line in lines:
        if len(line) < 10 or re.match(r'^[-=*•]+$', line):
            continue
        clean = line.lstrip('•-* ')
        if len(clean) > 8:
            achievements.append({'title': clean, 'description': ''})
    
    return achievements


def parse_resume(pdf_path: str) -> dict:
    """
    Main parser function.
    Returns a dict with all extracted sections.
    """
    logger.info(f"Parsing resume: {pdf_path}")
    logger.info(f"PDF readers available: pdfplumber={PDF_PLUMBER_AVAILABLE}, pypdf={PYPDF_AVAILABLE}")
    
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        return {'error': 'Could not extract text from PDF'}
    
    sections = split_into_sections(text)
    
    result = {
        'contact': extract_contact_info(sections.get('header', '') + sections.get('contact', '')),
        'summary': sections.get('summary', '').strip(),
        'education': extract_education(sections.get('education', '')),
        'skills': extract_skills(sections.get('skills', '')),
        'projects': extract_projects(sections.get('projects', '')),
        'certifications': extract_certifications(sections.get('certifications', '')),
        'achievements': extract_achievements(sections.get('achievements', '')),
        'raw_text_length': len(text),
        'sections_found': list(sections.keys()),
    }
    
    logger.info(f"Parsing complete. Sections found: {result['sections_found']}")
    return result


def save_parsed_data_to_db(parsed: dict, db_query_fn) -> dict:
    """
    Save parsed resume data to MySQL tables.
    db_query_fn should be models.database.query_db
    """
    results = {'updated': [], 'errors': []}
    
    # Update profile
    contact = parsed.get('contact', {})
    if contact.get('name') or contact.get('email'):
        try:
            db_query_fn(
                "UPDATE profile SET full_name=%s, email=%s, linkedin=%s, github=%s WHERE id=1",
                (
                    contact.get('name', 'Abhijeet V S'),
                    contact.get('email', ''),
                    contact.get('linkedin', ''),
                    contact.get('github', ''),
                ),
                commit=True
            )
            results['updated'].append('profile')
        except Exception as e:
            results['errors'].append(f"profile: {e}")
    
    # Skills
    skills = parsed.get('skills', [])
    if skills:
        try:
            for skill in skills[:30]:  # Cap at 30
                existing = db_query_fn(
                    "SELECT id FROM skills WHERE LOWER(name)=LOWER(%s)",
                    (skill['name'],), one=True
                )
                if not existing:
                    db_query_fn(
                        "INSERT INTO skills (name, category, proficiency) VALUES (%s, %s, %s)",
                        (skill['name'], skill['category'], skill.get('proficiency', 75)),
                        commit=True
                    )
            results['updated'].append('skills')
        except Exception as e:
            results['errors'].append(f"skills: {e}")
    
    # Education
    education = parsed.get('education', [])
    if education:
        try:
            for edu in education[:3]:
                db_query_fn(
                    "INSERT IGNORE INTO education (degree, institution, cgpa) VALUES (%s, %s, %s)",
                    (edu.get('degree', ''), edu.get('institution', ''), edu.get('cgpa', '')),
                    commit=True
                )
            results['updated'].append('education')
        except Exception as e:
            results['errors'].append(f"education: {e}")
    
    # Projects
    projects = parsed.get('projects', [])
    if projects:
        try:
            for proj in projects[:10]:
                existing = db_query_fn(
                    "SELECT id FROM projects WHERE LOWER(title)=LOWER(%s)",
                    (proj['title'],), one=True
                )
                if not existing and len(proj.get('title', '')) > 5:
                    db_query_fn(
                        "INSERT INTO projects (title, description, technologies, features) VALUES (%s,%s,%s,%s)",
                        (proj['title'], proj.get('description',''), proj.get('technologies',''), proj.get('features','')),
                        commit=True
                    )
            results['updated'].append('projects')
        except Exception as e:
            results['errors'].append(f"projects: {e}")
    
    # Certifications
    certs = parsed.get('certifications', [])
    if certs:
        try:
            for cert in certs[:10]:
                existing = db_query_fn(
                    "SELECT id FROM certifications WHERE LOWER(name)=LOWER(%s)",
                    (cert['name'],), one=True
                )
                if not existing and len(cert.get('name', '')) > 8:
                    db_query_fn(
                        "INSERT INTO certifications (name, issuer) VALUES (%s, %s)",
                        (cert['name'], cert.get('issuer', 'Unknown')),
                        commit=True
                    )
            results['updated'].append('certifications')
        except Exception as e:
            results['errors'].append(f"certifications: {e}")
    
    # Achievements
    achievements = parsed.get('achievements', [])
    if achievements:
        try:
            for ach in achievements[:10]:
                existing = db_query_fn(
                    "SELECT id FROM achievements WHERE LOWER(title)=LOWER(%s)",
                    (ach['title'],), one=True
                )
                if not existing and len(ach.get('title', '')) > 8:
                    db_query_fn(
                        "INSERT INTO achievements (title, description) VALUES (%s,%s)",
                        (ach['title'], ach.get('description', '')),
                        commit=True
                    )
            results['updated'].append('achievements')
        except Exception as e:
            results['errors'].append(f"achievements: {e}")
    
    return results
