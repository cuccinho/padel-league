from app import create_app
from app.extensions import db
from app.models import Player, Game
from datetime import datetime
import random

def seed_data():
    print("Clearing existing data...")
    Game.query.delete()
    Player.query.delete()
    db.session.commit()

    print("Adding players: ['Lars', 'Nils', 'Marcel', 'Flo']")
    players = [
        Player(name="Lars"),
        Player(name="Nils"),
        Player(name="Marcel"),
        Player(name="Flo")
    ]
    db.session.add_all(players)
    db.session.commit()

    # Fetch players with IDs from the database
    players = Player.query.all()
    player_ids = [p.id for p in players]
    print("Player IDs:", player_ids)

    # Generate matches
    print("Generating matches...")
    games = []
    for _ in range(50):  # Generate 50 matches
        random.shuffle(player_ids)
        team1 = player_ids[:2]
        team2 = player_ids[2:]
        score_team1 = random.randint(6, 7)  # Random valid Padel score
        score_team2 = random.randint(0, 6)
        if score_team1 == 7:
            score_team2 = random.randint(5, 6)  # 7-5 or 7-6 is valid

        new_game = Game(
            player1=Player.query.get(team1[0]),
            position1="Right",
            player2=Player.query.get(team1[1]),
            position2="Left",
            player3=Player.query.get(team2[0]),
            position3="Left",
            player4=Player.query.get(team2[1]),
            position4="Right",
            score_team1=score_team1,
            score_team2=score_team2,
            date=datetime.utcnow()
        )
        games.append(new_game)

    print(f"Adding {len(games)} matches to the database...")
    db.session.add_all(games)
    db.session.commit()
    print("Database seeded with example players and matches!")

if __name__ == "__main__":
    app = create_app()  # Create the Flask app
    with app.app_context():  # Wrap everything in an application context
        seed_data()
