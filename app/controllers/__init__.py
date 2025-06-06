from app.controllers.admin import admin_bp
from app.controllers.library import library_bp

def register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(library_bp)