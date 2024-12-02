from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime  # Import datetime for handling timestamps
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
        player_name = request.form["name"]
        new_player = Player(name=player_name)
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("main.players_list"))
    return render_template("add_player.html")

@main_bp.route("/games")
def games_list():
    from app.models import Game, Player
    games = Game.query.all()
    game_details = []

    # Fetch player names for each game
    for game in games:
        game_details.append({
            "id": game.id,
            "team1": [Player.query.get(game.player1).name, Player.query.get(game.player2).name],
            "team2": [Player.query.get(game.player3).name, Player.query.get(game.player4).name],
            "score_team1": game.score_team1,
            "score_team2": game.score_team2,
            "date": game.date
        })

    return render_template("games_list.html", games=game_details)

@main_bp.route("/games/add", methods=["GET", "POST"])
def add_game():
    from app.models import Player, Game
    from app.extensions import db
    players = Player.query.all()

    if request.method == "POST":
        player1 = request.form["player1"]
        player2 = request.form["player2"]
        player3 = request.form["player3"]
        player4 = request.form["player4"]
        score_team1 = request.form["score_team1"]
        score_team2 = request.form["score_team2"]

        new_game = Game(
            player1=player1,
            player2=player2,
            player3=player3,
            player4=player4,
            score_team1=score_team1,
            score_team2=score_team2,
            date=datetime.utcnow()
        )

        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for("main.games_list"))

    return render_template("add_game.html", players=players)
