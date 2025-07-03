from flask import Flask
from app.config import get_config
from app.extensions import db, migrate, cors, jwt
from app.admin import init_admin
from app.controllers.admin import admin_bp
from app.controllers.library import library_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.profile import profile_bp
from app.controllers.wishlist_item import wishlist_item_bp
from app.controllers.user_controller import user_bp
from app.controllers.steam_controller import steam_controller
from app.controllers.cart_controller import cart_controller
from app.error_handlers import register_error_handlers

def create_app(env: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS to allow all origins (simple and flexible)
    cors.init_app(app, 
                  origins="*",
                  allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"],
                  methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
                  supports_credentials=False,
                  automatic_options=True)
    
    jwt.init_app(app)
    init_admin(app)
    
    register_error_handlers(app)

    app.register_blueprint(admin_bp, url_prefix="/api/admins")
    app.register_blueprint(library_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api/profiles")
    app.register_blueprint(wishlist_item_bp, url_prefix="/api/wishlist")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(steam_controller)
    app.register_blueprint(cart_controller)

    @app.get("/ping")
    def ping():
        return {"status": "ok"}

    return app
