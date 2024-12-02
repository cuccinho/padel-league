import os
from flask import Flask
from app.extensions import db, migrate
from app.routes.main import main_bp

def create_app():
    # Initialize Flask application
    app = Flask(__name__, template_folder="templates")  # Explicitly set templates folder

    # Debugging statements
    print("Templates folder being used:", os.path.abspath('app/templates'))
    print("Index.html exists:", os.path.isfile(os.path.abspath('app/templates/index.html')))

    # Flask Configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///padel_league.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(main_bp)

    return app
