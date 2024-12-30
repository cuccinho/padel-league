import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'padel_league.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "a_very_secret_key"
    # Game Password
    GAME_PASSWORD = os.getenv("GAME_PASSWORD", "ratingen")  # Defaults to "ratingen"
