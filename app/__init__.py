import os
from flask import Flask
from app.extensions import db, migrate
from app.routes.main import main_bp
from app import models  # Import models to register them with Flask-Migrate
from config import Config  # Import the Config class from your config.py file


def create_app():
    # Initialize Flask application
    app = Flask(__name__, template_folder="templates")  # Explicitly set templates folder

    # Load configuration from Config class
    app.config.from_object(Config)

    # Debugging statements (optional)
    print("Templates folder being used:", os.path.abspath('app/templates'))
    print("Index.html exists:", os.path.isfile(os.path.abspath('app/templates/index.html')))
    print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"])

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(main_bp)

    return app
