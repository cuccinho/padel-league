from flask import Flask
from app.extensions import db
from app.routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)

    # Enable flash messages secret key
    app.secret_key = app.config['SECRET_KEY']

    return app
