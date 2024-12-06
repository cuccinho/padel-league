import os

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:////app/instance/padel_league.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret Key for Sessions
    SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key")

    # Game Password
    GAME_PASSWORD = os.getenv("GAME_PASSWORD", "ratingen")  # Defaults to "ratingen"
