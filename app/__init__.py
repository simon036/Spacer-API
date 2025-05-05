from flask import Flask, jsonify
from marshmallow import ValidationError
from .config import Config
from .extensions import db, migrate, jwt, ma, swagger, cors, limiter, cache
from .routes import auth_bp, spaces_bp, bookings_bp, users_bp
from .routes.admin import admin_bp
from .routes.google_auth import google_bp, google_auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    swagger.init_app(app)
    cors.init_app(app, origins=app.config.get("CORS_ORIGINS", "*").split(","))
    limiter.init_app(app)
    cache.init_app(app)

    # Register Flask-Dance Google blueprint
    app.register_blueprint(google_bp, url_prefix="/api/auth/google")
    app.register_blueprint(google_auth_bp, url_prefix="/api/auth/google")

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(spaces_bp, url_prefix='/api/spaces')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # Error handlers
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"errors": e.messages}), 400
        
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app
