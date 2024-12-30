from app.extensions import db
from datetime import datetime

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player3_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player4_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)

    player1 = db.relationship('Player', foreign_keys=[player1_id])
    player2 = db.relationship('Player', foreign_keys=[player2_id])
    player3 = db.relationship('Player', foreign_keys=[player3_id])
    player4 = db.relationship('Player', foreign_keys=[player4_id])

    position1 = db.Column(db.String(10), nullable=False)
    position2 = db.Column(db.String(10), nullable=False)
    position3 = db.Column(db.String(10), nullable=False)
    position4 = db.Column(db.String(10), nullable=False)

    score_team1 = db.Column(db.Integer, nullable=False)
    score_team2 = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class AmericanoTournament(db.Model):
    __tablename__ = 'americano_tournaments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    num_courts = db.Column(db.Integer, nullable=False)

    players = db.relationship('AmericanoPlayer', backref='tournament', lazy=True)
    games = db.relationship('AmericanoGame', backref='tournament', lazy=True)

class AmericanoPlayer(db.Model):
    __tablename__ = 'americano_players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('americano_tournaments.id'), nullable=False)

class AmericanoGame(db.Model):
    __tablename__ = 'americano_games'
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('americano_players.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('americano_players.id'), nullable=False)
    player3_id = db.Column(db.Integer, db.ForeignKey('americano_players.id'), nullable=False)
    player4_id = db.Column(db.Integer, db.ForeignKey('americano_players.id'), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('americano_tournaments.id'), nullable=False)

    player1 = db.relationship('AmericanoPlayer', foreign_keys=[player1_id])
    player2 = db.relationship('AmericanoPlayer', foreign_keys=[player2_id])
    player3 = db.relationship('AmericanoPlayer', foreign_keys=[player3_id])
    player4 = db.relationship('AmericanoPlayer', foreign_keys=[player4_id])

    score_team1 = db.Column(db.Integer, nullable=True)  # Allow null for unplayed matches
    score_team2 = db.Column(db.Integer, nullable=True)  # Allow null for unplayed matches
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
