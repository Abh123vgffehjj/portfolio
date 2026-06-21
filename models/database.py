import mysql.connector
import os
from flask import current_app, g


def get_db_config():
    return {
        'host': os.environ.get('MYSQL_HOST', 'thomas.proxy.rlwy.net'),
        'port': int(os.environ.get('MYSQL_PORT', 26171)),
        'user': os.environ.get('MYSQL_USER', 'root'),
        'password': os.environ.get('MYSQL_PASSWORD', 'wEcvGAtWURCqXfwbEQHwgMAzMRgbUeEC'),
        'database': os.environ.get('MYSQL_DATABASE', 'railway'),
        'charset': 'utf8mb4',
        'use_unicode': True,
        'autocommit': False,
        'connection_timeout': 10,
    }


def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(**get_db_config())
        except mysql.connector.Error as e:
            current_app.logger.error(f"Database connection failed: {e}")
            raise
    else:
        # Reconnect if connection was dropped
        try:
            g.db.ping(reconnect=True, attempts=3, delay=1)
        except mysql.connector.Error:
            try:
                g.db = mysql.connector.connect(**get_db_config())
            except mysql.connector.Error as e:
                current_app.logger.error(f"Database reconnect failed: {e}")
                raise
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        try:
            if db.is_connected():
                db.close()
        except Exception:
            pass


def query_db(query, args=(), one=False, commit=False):
    """Execute a query and return results as dicts."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(query, args)
        if commit:
            db.commit()
            return cursor.lastrowid
        rv = cursor.fetchall()
        return (rv[0] if rv else None) if one else rv
    except mysql.connector.Error as e:
        if commit:
            try:
                db.rollback()
            except Exception:
                pass
        current_app.logger.error(f"DB query error: {e} | Query: {query[:200]}")
        raise
    finally:
        cursor.close()


def init_app(app):
    app.teardown_appcontext(close_db)
