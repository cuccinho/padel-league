from app.extensions import db

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # Name must be unique
    active = db.Column(db.Boolean, default=True)

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    player1 = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player2 = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player3 = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player4 = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    position1 = db.Column(db.String(10), nullable=False)
    position2 = db.Column(db.String(10), nullable=False)
    position3 = db.Column(db.String(10), nullable=False)
    position4 = db.Column(db.String(10), nullable=False)
    score_team1 = db.Column(db.Integer, nullable=False)
    score_team2 = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

