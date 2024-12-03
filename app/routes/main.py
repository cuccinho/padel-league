from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Player, Game

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/players")
def players_list():
    players = Player.query.all()
    return render_template("players_list.html", players=players)

@main_bp.route("/games")
def games_list():
    games = Game.query.all()
    players = Player.query.all()

    # Generate player combination stats dynamically from the database
    player_combination_stats = {}
    for game in games:
        combination = f"{game.player1.name} & {game.player2.name} vs {game.player3.name} & {game.player4.name}"
        if combination not in player_combination_stats:
            player_combination_stats[combination] = {
                "wins": 0,
                "losses": 0,
                "points_won": 0,
                "points_lost": 0,
            }
        # Update stats based on the game's score
        if game.score_team1 > game.score_team2:
            player_combination_stats[combination]["wins"] += 1
            player_combination_stats[combination]["points_won"] += game.score_team1
            player_combination_stats[combination]["points_lost"] += game.score_team2
        else:
            player_combination_stats[combination]["losses"] += 1
            player_combination_stats[combination]["points_won"] += game.score_team2
            player_combination_stats[combination]["points_lost"] += game.score_team1

    return render_template(
        "games_list.html",
        games=games,
        players=players,
        player_combination_stats=player_combination_stats
    )
