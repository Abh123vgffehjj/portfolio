"""
Admin Dashboard Routes
"""
import os
import json
from datetime import datetime
from functools import wraps
from flask import (Blueprint, render_template, request, jsonify, session,
                   redirect, url_for, current_app, flash)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from models.database import query_db
from resume_parser.parser import parse_resume, save_parsed_data_to_db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# ── Inject unread_count into all admin templates ──────────────────
@admin_bp.context_processor
def inject_unread_count():
    if session.get('admin_logged_in'):
        try:
            result = query_db("SELECT COUNT(*) as c FROM contacts WHERE is_read=0", one=True)
            unread_count = result['c'] if result else 0
        except Exception:
            unread_count = 0
    else:
        unread_count = 0
    return {'unread_count': unread_count}


def _format_datetime(dt):
    """Safely format a datetime value that may be a string or datetime object."""
    if dt is None:
        return 'N/A'
    if isinstance(dt, str):
        try:
            dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return dt
    if hasattr(dt, 'strftime'):
        return dt.strftime('%b %d, %Y')
    return str(dt)


def _format_datetime_full(dt):
    """Safely format datetime with time."""
    if dt is None:
        return '—'
    if isinstance(dt, str):
        try:
            dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return dt
    if hasattr(dt, 'strftime'):
        return dt.strftime('%b %d, %Y %H:%M')
    return str(dt)


# ── Auth decorator ────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


# ── Login / Logout ────────────────────────────────────────────────────────────
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        valid = False
        try:
            # Check DB first
            admin = query_db("SELECT * FROM admin_users WHERE username=%s", (username,), one=True)
            if admin:
                valid = check_password_hash(admin['password_hash'], password)
            else:
                # Not in DB — fall back to env vars
                valid = (
                    username == current_app.config['ADMIN_USERNAME'] and
                    password == current_app.config['ADMIN_PASSWORD']
                )
        except Exception:
            # DB unreachable — use env var credentials only
            valid = (
                username == current_app.config['ADMIN_USERNAME'] and
                password == current_app.config['ADMIN_PASSWORD']
            )
        
        if valid:
            session.permanent = True
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('admin/login.html')


@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


# ── Dashboard ─────────────────────────────────────────────────────────────────
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    def safe_count(sql):
        try:
            result = query_db(sql, one=True)
            return result['c'] if result else 0
        except Exception:
            return 0

    stats = {
        'projects':       safe_count("SELECT COUNT(*) as c FROM projects"),
        'skills':         safe_count("SELECT COUNT(*) as c FROM skills"),
        'certifications': safe_count("SELECT COUNT(*) as c FROM certifications"),
        'contacts':       safe_count("SELECT COUNT(*) as c FROM contacts"),
        'unread_contacts':safe_count("SELECT COUNT(*) as c FROM contacts WHERE is_read=0"),
        'visitors':       safe_count("SELECT COUNT(*) as c FROM visitors"),
        'achievements':   safe_count("SELECT COUNT(*) as c FROM achievements"),
        'resumes':        safe_count("SELECT COUNT(*) as c FROM resume_uploads"),
    }
    try:
        recent_contacts = query_db(
            "SELECT * FROM contacts ORDER BY created_at DESC LIMIT 5"
        )
    except Exception:
        recent_contacts = []

    try:
        recent_visitors = query_db(
            "SELECT DATE(visited_at) as date, COUNT(*) as count "
            "FROM visitors GROUP BY DATE(visited_at) ORDER BY date DESC LIMIT 7"
        )
    except Exception:
        recent_visitors = []

    return render_template('admin/dashboard.html', stats=stats,
                           recent_contacts=recent_contacts,
                           recent_visitors=recent_visitors)



# ── Resume Upload & Parse ─────────────────────────────────────────────────────
@admin_bp.route('/upload-resume', methods=['GET', 'POST'])
@login_required
def upload_resume():
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file selected.', 'error')
            return redirect(request.url)

        file = request.files['resume']
        if not file.filename:
            flash('No file selected.', 'error')
            return redirect(request.url)

        if not file.filename.lower().endswith('.pdf'):
            flash('Only PDF files are allowed.', 'error')
            return redirect(request.url)

        try:
            import tempfile
            filename = secure_filename(file.filename)
            file_bytes = file.read()
            file_size = len(file_bytes)

            # Save to temp file (works on Vercel serverless)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            # Record upload in DB
            try:
                upload_id = query_db(
                    "INSERT INTO resume_uploads (filename, original_filename, file_size, parse_status) VALUES (%s,%s,%s,'uploaded')",
                    (filename, file.filename, file_size),
                    commit=True
                )
            except Exception:
                upload_id = None

            # Parse the temp file
            try:
                parsed = parse_resume(tmp_path)
                if 'error' not in parsed:
                    results = save_parsed_data_to_db(parsed, query_db)
                    if upload_id:
                        query_db(
                            "UPDATE resume_uploads SET parsed=1, parse_status='success', parse_log=%s WHERE id=%s",
                            (json.dumps(results), upload_id),
                            commit=True
                        )
                    flash(f'Resume parsed! Updated: {", ".join(results["updated"])}', 'success')
                else:
                    flash(f'Upload ok but parsing failed: {parsed["error"]}', 'warning')
            except Exception as e:
                flash(f'Parsing error: {str(e)}', 'error')
            finally:
                # Always delete temp file
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

        except Exception as e:
            flash(f'Upload error: {str(e)}', 'error')

        return redirect(url_for('admin.upload_resume'))

    try:
        uploads = query_db("SELECT * FROM resume_uploads ORDER BY uploaded_at DESC LIMIT 20")
    except Exception:
        uploads = []
    return render_template('admin/upload_resume.html', uploads=uploads)

# ── Projects CRUD ─────────────────────────────────────────────────────────────
@admin_bp.route('/projects')
@login_required
def projects():
    items = query_db("SELECT * FROM projects ORDER BY display_order, id")
    return render_template('admin/projects.html', items=items)


@admin_bp.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        data = request.form
        query_db(
            "INSERT INTO projects (title,description,technologies,features,achievement,github_url,live_url,category,is_featured,display_order) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (data['title'], data['description'], data.get('technologies',''), data.get('features',''),
             data.get('achievement',''), data.get('github_url',''), data.get('live_url',''),
             data.get('category',''), 1 if data.get('is_featured') else 0, int(data.get('display_order', 0))),
            commit=True
        )
        flash('Project added!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', item=None)


@admin_bp.route('/projects/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_project(item_id):
    item = query_db("SELECT * FROM projects WHERE id=%s", (item_id,), one=True)
    if not item:
        flash('Project not found.', 'error')
        return redirect(url_for('admin.projects'))
    
    if request.method == 'POST':
        data = request.form
        query_db(
            "UPDATE projects SET title=%s,description=%s,technologies=%s,features=%s,achievement=%s,github_url=%s,live_url=%s,category=%s,is_featured=%s,display_order=%s WHERE id=%s",
            (data['title'], data['description'], data.get('technologies',''), data.get('features',''),
             data.get('achievement',''), data.get('github_url',''), data.get('live_url',''),
             data.get('category',''), 1 if data.get('is_featured') else 0, int(data.get('display_order', 0)), item_id),
            commit=True
        )
        flash('Project updated!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', item=item)


@admin_bp.route('/projects/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_project(item_id):
    query_db("DELETE FROM projects WHERE id=%s", (item_id,), commit=True)
    flash('Project deleted.', 'success')
    return redirect(url_for('admin.projects'))


# ── Skills CRUD ───────────────────────────────────────────────────────────────
@admin_bp.route('/skills')
@login_required
def skills():
    items = query_db("SELECT * FROM skills ORDER BY category, name")
    return render_template('admin/skills.html', items=items)


@admin_bp.route('/skills/add', methods=['POST'])
@login_required
def add_skill():
    data = request.form
    query_db(
        "INSERT INTO skills (name,category,proficiency) VALUES (%s,%s,%s)",
        (data['name'], data['category'], int(data.get('proficiency', 80))),
        commit=True
    )
    flash('Skill added!', 'success')
    return redirect(url_for('admin.skills'))


@admin_bp.route('/skills/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_skill(item_id):
    query_db("DELETE FROM skills WHERE id=%s", (item_id,), commit=True)
    flash('Skill deleted.', 'success')
    return redirect(url_for('admin.skills'))


# ── Certifications CRUD ───────────────────────────────────────────────────────
@admin_bp.route('/certifications')
@login_required
def certifications():
    items = query_db("SELECT * FROM certifications ORDER BY display_order, id")
    return render_template('admin/certifications.html', items=items)


@admin_bp.route('/certifications/add', methods=['POST'])
@login_required
def add_certification():
    data = request.form
    query_db(
        "INSERT INTO certifications (name,issuer,issue_date,description,display_order) VALUES (%s,%s,%s,%s,%s)",
        (data['name'], data.get('issuer',''), data.get('issue_date',''), data.get('description',''), int(data.get('display_order',0))),
        commit=True
    )
    flash('Certification added!', 'success')
    return redirect(url_for('admin.certifications'))


@admin_bp.route('/certifications/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_certification(item_id):
    query_db("DELETE FROM certifications WHERE id=%s", (item_id,), commit=True)
    flash('Certification deleted.', 'success')
    return redirect(url_for('admin.certifications'))


# ── Achievements CRUD ─────────────────────────────────────────────────────────
@admin_bp.route('/achievements')
@login_required
def achievements():
    items = query_db("SELECT * FROM achievements ORDER BY display_order, id")
    return render_template('admin/achievements.html', items=items)


@admin_bp.route('/achievements/add', methods=['POST'])
@login_required
def add_achievement():
    data = request.form
    query_db(
        "INSERT INTO achievements (title,description,date,display_order) VALUES (%s,%s,%s,%s)",
        (data['title'], data.get('description',''), data.get('date',''), int(data.get('display_order',0))),
        commit=True
    )
    flash('Achievement added!', 'success')
    return redirect(url_for('admin.achievements'))


@admin_bp.route('/achievements/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_achievement(item_id):
    query_db("DELETE FROM achievements WHERE id=%s", (item_id,), commit=True)
    flash('Achievement deleted.', 'success')
    return redirect(url_for('admin.achievements'))


# ── Contact Messages ──────────────────────────────────────────────────────────
@admin_bp.route('/contacts')
@login_required
def contacts():
    try:
        items = query_db("SELECT * FROM contacts ORDER BY created_at DESC")
        query_db("UPDATE contacts SET is_read=1", commit=True)
    except Exception:
        items = []
    return render_template('admin/contacts.html', items=items)


@admin_bp.route('/contacts/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_contact(item_id):
    try:
        query_db("DELETE FROM contacts WHERE id=%s", (item_id,), commit=True)
        flash('Message deleted.', 'success')
    except Exception as e:
        flash(f'Error deleting message: {e}', 'error')
    return redirect(url_for('admin.contacts'))


# ── Visitor Analytics ─────────────────────────────────────────────────────────
@admin_bp.route('/analytics')
@login_required
def analytics():
    try:
        daily = query_db(
            "SELECT DATE(visited_at) as date, COUNT(*) as count "
            "FROM visitors GROUP BY DATE(visited_at) ORDER BY date DESC LIMIT 30"
        )
        # Convert date objects to strings for JSON serialisation in template
        daily = [{'date': str(r['date']), 'count': int(r['count'])} for r in daily]
    except Exception:
        daily = []

    try:
        total = query_db("SELECT COUNT(*) as c FROM visitors", one=True)
        total = total['c'] if total else 0
    except Exception:
        total = 0

    try:
        today_row = query_db(
            "SELECT COUNT(*) as c FROM visitors WHERE DATE(visited_at)=CURDATE()", one=True
        )
        today = today_row['c'] if today_row else 0
    except Exception:
        today = 0

    return render_template('admin/analytics.html', daily=daily, total=total, today=today)
