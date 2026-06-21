"""
Public API Routes for Portfolio
"""
import os
import json
from flask import Blueprint, jsonify, request, current_app
from models.database import query_db

api_bp = Blueprint('api', __name__, url_prefix='/api')


def _parse_list_field(value, sep=','):
    """Convert a stored string to a Python list."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return parsed
    except (json.JSONDecodeError, TypeError):
        pass
    return [s.strip() for s in value.split(sep) if s.strip()]


def _jsonify_row(row):
    """Post-process a DB row dict: parse JSON/CSV fields into lists."""
    if row is None:
        return row
    if isinstance(row, list):
        return [_jsonify_row(r) for r in row]
    result = dict(row)
    # animated_roles is a JSON array
    if 'animated_roles' in result:
        result['animated_roles'] = _parse_list_field(result['animated_roles'])
    # technologies and features: comma or newline separated
    if 'technologies' in result:
        result['technologies'] = _parse_list_field(result['technologies'])
    if 'features' in result:
        result['features'] = _parse_list_field(result['features'], sep='\n')
    # Convert datetime objects to strings
    for key, val in result.items():
        if hasattr(val, 'isoformat'):
            result[key] = str(val)
    return result


def api_error(msg, code=500):
    return jsonify({'error': msg}), code


# ── Profile ───────────────────────────────────────────────────────
@api_bp.route('/profile')
def get_profile():
    try:
        row = query_db("SELECT * FROM profile WHERE id=1", one=True)
        if not row:
            return api_error('Profile not found', 404)
        return jsonify(_jsonify_row(row))
    except Exception as e:
        current_app.logger.error(f"GET /api/profile: {e}")
        return api_error('Database error', 500)


# ── Education ─────────────────────────────────────────────────────
@api_bp.route('/education')
def get_education():
    try:
        rows = query_db("SELECT * FROM education ORDER BY id ASC")
        return jsonify(rows)
    except Exception as e:
        current_app.logger.error(f"GET /api/education: {e}")
        return api_error('Database error', 500)


# ── Skills ────────────────────────────────────────────────────────
@api_bp.route('/skills')
def get_skills():
    try:
        rows = query_db("SELECT * FROM skills ORDER BY category, name")
        grouped = {}
        for row in rows:
            cat = row['category']
            grouped.setdefault(cat, []).append(row)
        return jsonify({'grouped': grouped, 'all': rows})
    except Exception as e:
        current_app.logger.error(f"GET /api/skills: {e}")
        return api_error('Database error', 500)


# ── Projects ──────────────────────────────────────────────────────
@api_bp.route('/projects')
def get_projects():
    try:
        category = request.args.get('category', '').strip()
        search   = request.args.get('search', '').strip()

        if category:
            rows = query_db(
                "SELECT * FROM projects WHERE category=%s ORDER BY is_featured DESC, display_order, id",
                (category,)
            )
        elif search:
            like = f'%{search}%'
            rows = query_db(
                """SELECT * FROM projects
                   WHERE title LIKE %s OR description LIKE %s OR technologies LIKE %s
                   ORDER BY is_featured DESC, display_order, id""",
                (like, like, like)
            )
        else:
            rows = query_db(
                "SELECT * FROM projects ORDER BY is_featured DESC, display_order, id"
            )
        return jsonify([_jsonify_row(r) for r in rows])
    except Exception as e:
        current_app.logger.error(f"GET /api/projects: {e}")
        return api_error('Database error', 500)


@api_bp.route('/projects/<int:project_id>')
def get_project(project_id):
    try:
        row = query_db("SELECT * FROM projects WHERE id=%s", (project_id,), one=True)
        if not row:
            return api_error('Not found', 404)
        return jsonify(_jsonify_row(row))
    except Exception as e:
        current_app.logger.error(f"GET /api/projects/{project_id}: {e}")
        return api_error('Database error', 500)


# ── Certifications ────────────────────────────────────────────────
@api_bp.route('/certifications')
def get_certifications():
    try:
        rows = query_db("SELECT * FROM certifications ORDER BY display_order, id")
        return jsonify(rows)
    except Exception as e:
        current_app.logger.error(f"GET /api/certifications: {e}")
        return api_error('Database error', 500)


# ── Achievements ──────────────────────────────────────────────────
@api_bp.route('/achievements')
def get_achievements():
    try:
        rows = query_db("SELECT * FROM achievements ORDER BY display_order, id")
        return jsonify(rows)
    except Exception as e:
        current_app.logger.error(f"GET /api/achievements: {e}")
        return api_error('Database error', 500)


# ── Project categories ────────────────────────────────────────────
@api_bp.route('/project-categories')
def get_project_categories():
    try:
        rows = query_db(
            "SELECT DISTINCT category FROM projects WHERE category IS NOT NULL AND category != ''"
        )
        return jsonify([r['category'] for r in rows])
    except Exception as e:
        current_app.logger.error(f"GET /api/project-categories: {e}")
        return api_error('Database error', 500)


# ── Visitor Counter ───────────────────────────────────────────────
@api_bp.route('/visitor-count')
def get_visitor_count():
    try:
        result = query_db("SELECT COUNT(*) as count FROM visitors", one=True)
        return jsonify({'count': result['count'] if result else 0})
    except Exception as e:
        current_app.logger.error(f"GET /api/visitor-count: {e}")
        return jsonify({'count': 0})


@api_bp.route('/record-visit', methods=['POST'])
def record_visit():
    ip   = request.headers.get('X-Forwarded-For', request.remote_addr or '')
    ip   = ip.split(',')[0].strip()[:50]
    ua   = (request.headers.get('User-Agent', '') or '')[:500]
    page = '/'
    if request.is_json:
        page = (request.get_json(silent=True) or {}).get('page', '/')
    page = str(page)[:200]
    try:
        query_db(
            "INSERT INTO visitors (ip_address, user_agent, page) VALUES (%s, %s, %s)",
            (ip, ua, page),
            commit=True
        )
        return jsonify({'ok': True})
    except Exception as e:
        current_app.logger.warning(f"record-visit error: {e}")
        return jsonify({'ok': False}), 500


# ── Contact Form ──────────────────────────────────────────────────
@api_bp.route('/contact', methods=['POST'])
def submit_contact():
    data    = request.get_json(force=True, silent=True) or {}
    name    = str(data.get('name', '')).strip()
    email   = str(data.get('email', '')).strip()
    message = str(data.get('message', '')).strip()

    # Validation
    errors = []
    if not name or len(name) < 2:
        errors.append('Please enter your full name (at least 2 characters).')
    if not email or '@' not in email or '.' not in email.split('@')[-1]:
        errors.append('Please enter a valid email address.')
    if not message or len(message) < 10:
        errors.append('Message must be at least 10 characters.')
    if len(message) > 2000:
        errors.append('Message is too long (max 2000 characters).')
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    # Spam check
    spam_keywords = ['buy now', 'click here', 'free money', 'cryptocurrency',
                     'bitcoin', 'casino', 'lottery', 'prize']
    if any(kw in message.lower() for kw in spam_keywords):
        return jsonify({'success': False, 'errors': ['Message flagged as spam.']}), 400

    ip = (request.headers.get('X-Forwarded-For', request.remote_addr) or '').split(',')[0].strip()[:50]
    try:
        query_db(
            "INSERT INTO contacts (name, email, message, ip_address) VALUES (%s, %s, %s, %s)",
            (name[:200], email[:200], message[:2000], ip),
            commit=True
        )
        return jsonify({
            'success': True,
            'message': "Message sent successfully! I'll get back to you soon. 🕷️"
        })
    except Exception as e:
        current_app.logger.error(f"POST /api/contact save error: {e}")
        return jsonify({'success': False, 'errors': ['Server error. Please try again later.']}), 500
