import os
from flask import Flask
from app.extensions import db, migrate
from app.routes.main import main_bp
from config import Config  # Import the Config class from your config.py file

def create_app():
    app = Flask(__name__, template_folder="templates")

    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(main_bp)

    return app
