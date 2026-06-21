"""
WSGI entry point for production deployment.
Gunicorn uses this file: gunicorn wsgi:application
"""
from app import create_app

application = create_app('production')

if __name__ == '__main__':
    application.run()
