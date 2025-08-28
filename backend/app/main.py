from flask import Flask
from flask_jwt_extended import JWTManager
from app.interface.api.routes import register_routes
from app.interface.api.auth import auth_bp
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize JWT
    JWTManager(app)

    # Register all API route blueprints with their own prefixes
    register_routes(app)

    # Auth blueprint has no prefix defined; mount under /api/auth
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)