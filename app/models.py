from app.extensions import db

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # Name must be unique
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
