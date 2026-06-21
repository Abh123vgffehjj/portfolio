"""
Abhijeet V S - Portfolio Flask Application
Spider-Verse Themed Personal Portfolio
"""
import os
from flask import Flask, render_template, send_from_directory, Response
from config import config
from models import database
from routes.api import api_bp
from routes.admin import admin_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'production')
        if config_name not in ('development', 'production'):
            config_name = 'production'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Init database teardown
    database.init_app(app)

    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    # ── Main routes ───────────────────────────────────────────────
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/resume')
    def download_resume():
        resume_dir = os.path.join(app.root_path, 'static', 'resume')
        resume_path = os.path.join(resume_dir, 'resume.pdf')
        if not os.path.exists(resume_path):
            return "Resume PDF not found. Please add resume.pdf to static/resume/", 404
        return send_from_directory(
            resume_dir,
            'resume.pdf',
            as_attachment=True,
            download_name='Abhijeet_VS_Resume.pdf'
        )

    @app.route('/sitemap.xml')
    def sitemap():
        sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://abhijeetvs.vercel.app/</loc><priority>1.0</priority></url>
  <url><loc>https://abhijeetvs.vercel.app/#about</loc><priority>0.8</priority></url>
  <url><loc>https://abhijeetvs.vercel.app/#projects</loc><priority>0.9</priority></url>
  <url><loc>https://abhijeetvs.vercel.app/#skills</loc><priority>0.7</priority></url>
  <url><loc>https://abhijeetvs.vercel.app/#contact</loc><priority>0.8</priority></url>
</urlset>'''
        return Response(sitemap_xml, mimetype='application/xml')

    @app.route('/robots.txt')
    def robots():
        txt = ('User-agent: *\n'
               'Allow: /\n'
               'Disallow: /admin/\n'
               'Sitemap: https://abhijeetvs.vercel.app/sitemap.xml')
        return Response(txt, mimetype='text/plain')

    # ── Error handlers ────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error(f"500 error: {e}")
        return render_template('500.html'), 500

    # ── Security headers ──────────────────────────────────────────
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        if app.config.get('DEBUG') is False:
            response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
