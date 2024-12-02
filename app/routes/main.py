from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from app.models import Player, Game
from app.extensions import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/players")
def players_list():
    players = Player.query.all()
    return render_template("players_list.html", players=players)

@main_bp.route("/players/add", methods=["GET", "POST"])
def add_player():
    if request.method == "POST":
        name = request.form["name"]
        new_player = Player(name=name)
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("main.players_list"))
    return render_template("add_player.html")

@main_bp.route("/players/toggle/<int:player_id>", methods=["POST"])
def toggle_player(player_id):
    player = Player.query.get(player_id)
    if player:
        player.active = not player.active
        db.session.commit()
    return redirect(url_for("main.players_list"))

@main_bp.route("/games")
def games_list():
    games = Game.query.all()
    game_details = []
    player_combinations = {}

    # Fetch game details and calculate player statistics
    for game in games:
        team1 = [
            {"id": game.player1, "name": Player.query.get(game.player1).name, "position": game.position1},
            {"id": game.player2, "name": Player.query.get(game.player2).name, "position": game.position2}
        ]
        team2 = [
            {"id": game.player3, "name": Player.query.get(game.player3).name, "position": game.position3},
            {"id": game.player4, "name": Player.query.get(game.player4).name, "position": game.position4}
        ]

        game_details.append({
            "id": game.id,
            "team1": team1,
            "team2": team2,
            "score_team1": game.score_team1,
            "score_team2": game.score_team2,
            "date": game.date.strftime("%Y-%m-%d")  # Format date for frontend
        })

        # Process player combinations for both teams
        for team, opponent, score, opponent_score in [
            (team1, team2, game.score_team1, game.score_team2),
            (team2, team1, game.score_team2, game.score_team1),
        ]:
            key = f"{team[0]['name']} ({team[0]['position']}) + {team[1]['name']} ({team[1]['position']})"
            if key not in player_combinations:
                player_combinations[key] = {
                    "games": 0,
                    "won": 0,
                    "lost": 0,
                    "points_won": 0,
                    "points_lost": 0,
                }
            player_combinations[key]["games"] += 1
            player_combinations[key]["points_won"] += score
            player_combinations[key]["points_lost"] += opponent_score
            if score > opponent_score:
                player_combinations[key]["won"] += 1
            else:
                player_combinations[key]["lost"] += 1

    # Sort player combinations alphabetically for display
    player_combinations = dict(sorted(player_combinations.items()))

    return render_template(
        "games_list.html",
        games=game_details,
        total_games=len(games),
        player_combinations=player_combinations
    )

@main_bp.route("/games/add", methods=["GET", "POST"])
def add_game():
    players = Player.query.all()

    if request.method == "POST":
        player1 = request.form["player1"]
        player2 = request.form["player2"]
        player3 = request.form["player3"]
        player4 = request.form["player4"]
        position1 = request.form["position1"]
        position2 = request.form["position2"]
        position3 = request.form["position3"]
        position4 = request.form["position4"]
        score_team1 = request.form["score_team1"]
        score_team2 = request.form["score_team2"]

        new_game = Game(
            player1=player1,
            position1=position1,
            player2=player2,
            position2=position2,
            player3=player3,
            position3=position3,
            player4=player4,
            position4=position4,
            score_team1=score_team1,
            score_team2=score_team2,
            date=datetime.utcnow()
        )
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for("main.games_list"))

    return render_template("add_game.html", players=players)

@main_bp.route("/games/reset", methods=["POST"])
def reset_games():
    Game.query.delete()
    db.session.commit()
    return redirect(url_for("main.games_list"))
