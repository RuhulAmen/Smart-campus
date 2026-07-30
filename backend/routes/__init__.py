from flask import Blueprint

from .auth import auth_bp
from .facilities import facilities_bp
from .announcements import announcements_bp
from .issues import issues_bp
from .dashboard import dashboard_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(facilities_bp, url_prefix='/api/facilities')
    app.register_blueprint(announcements_bp, url_prefix='/api/announcements')
    app.register_blueprint(issues_bp, url_prefix='/api/issues')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')