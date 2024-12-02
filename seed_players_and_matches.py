from app.extensions import db
from app.models import Player, Game
from datetime import datetime
from app import create_app
import random

# Create Flask app and set up the application context
app = create_app()

def generate_valid_score():
    """Generates a valid padel score."""
    valid_scores = [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (7, 5), (7, 6)]
    return random.choice(valid_scores)

def seed_data():
    with app.app_context():
        # Clear existing players and games
        print("Clearing existing data...")
        Game.query.delete()
        Player.query.delete()
        db.session.commit()

        # Add players
        player_names = ["Lars", "Nils", "Marcel", "Flo"]
        print(f"Adding players: {player_names}")
        players = []
        for name in player_names:
            player = Player(name=name, active=True)
            db.session.add(player)
            players.append(player)
        db.session.commit()

        # Fetch player IDs
        player_ids = [player.id for player in Player.query.all()]
        print(f"Player IDs: {player_ids}")

        # Generate multiple matches with varying configurations
        games = []
        for i in range(50):  # Generate 50 matches
            positions = ["Right", "Left", "Right", "Left"]
            random.shuffle(positions)  # Randomize positions

            # Generate valid scores
            score_team1, score_team2 = generate_valid_score()

            # Create a game
            game = Game(
                player1=player_ids[0], position1=positions[0],
                player2=player_ids[1], position2=positions[1],
                player3=player_ids[2], position3=positions[2],
                player4=player_ids[3], position4=positions[3],
                score_team1=score_team1,
                score_team2=score_team2,
                date=datetime.utcnow()
            )
            games.append(game)
            print(f"Match {i+1}: {player_ids} with score {score_team1}-{score_team2}")

        # Add matches to the database
        print(f"Adding {len(games)} matches to the database...")
        db.session.add_all(games)
        db.session.commit()

        print(f"Added {len(player_names)} players and {len(games)} matches.")

if __name__ == "__main__":
    seed_data()
