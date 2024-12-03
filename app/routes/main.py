from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Player, Game
from app.extensions import db
from datetime import datetime

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    players = Player.query.all()

    player_combination_stats = {}

    # Compute player combinations and stats
    games = Game.query.all()
    for game in games:
        team1_combo = f"{game.player1.name} & {game.player2.name}"
        team2_combo = f"{game.player3.name} & {game.player4.name}"

        if team1_combo not in player_combination_stats:
            player_combination_stats[team1_combo] = {"wins": 0, "losses": 0, "points_won": 0, "points_lost": 0}
        if team2_combo not in player_combination_stats:
            player_combination_stats[team2_combo] = {"wins": 0, "losses": 0, "points_won": 0, "points_lost": 0}

        if game.score_team1 > game.score_team2:
            player_combination_stats[team1_combo]["wins"] += 1
            player_combination_stats[team2_combo]["losses"] += 1
        else:
            player_combination_stats[team2_combo]["wins"] += 1
            player_combination_stats[team1_combo]["losses"] += 1

        player_combination_stats[team1_combo]["points_won"] += game.score_team1
        player_combination_stats[team1_combo]["points_lost"] += game.score_team2
        player_combination_stats[team2_combo]["points_won"] += game.score_team2
        player_combination_stats[team2_combo]["points_lost"] += game.score_team1

    return render_template(
        "index.html",
        players=players,
        player_combination_stats=player_combination_stats
    )

@main_bp.route("/players")
def players_list():
    players = Player.query.all()
    return render_template("players_list.html", players=players)

@main_bp.route("/games")
def games_list():
    games = Game.query.all()
    players = Player.query.all()
    return render_template("games_list.html", games=games, players=players)

@main_bp.route("/games/add", methods=["GET", "POST"])
def add_game():
    players = Player.query.all()

    if request.method == "POST":
        player1_id = request.form["player1"]
        player2_id = request.form["player2"]
        player3_id = request.form["player3"]
        player4_id = request.form["player4"]
        position1 = request.form["position1"]
        position2 = request.form["position2"]
        position3 = request.form["position3"]
        position4 = request.form["position4"]
        score_team1 = int(request.form["score_team1"])
        score_team2 = int(request.form["score_team2"])

        # Check for invalid or duplicate selections
        selected_players = [player1_id, player2_id, player3_id, player4_id]
        selected_positions_team1 = [position1, position2]
        selected_positions_team2 = [position3, position4]

        if len(set(selected_players)) != 4:
            return render_template("add_game.html", players=players, error="Each player must be unique.")

        if len(set(selected_positions_team1)) != 2 or len(set(selected_positions_team2)) != 2:
            return render_template("add_game.html", players=players, error="Each team must have unique positions.")

        new_game = Game(
            player1_id=player1_id,
            position1=position1,
            player2_id=player2_id,
            position2=position2,
            player3_id=player3_id,
            position3=position3,
            player4_id=player4_id,
            position4=position4,
            score_team1=score_team1,
            score_team2=score_team2,
            date=datetime.utcnow()
        )
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for("main.games_list"))

    return render_template("add_game.html", players=players, error=None)

@main_bp.route("/games/reset", methods=["POST"])
def reset_games():
    Game.query.delete()
    db.session.commit()
    return redirect(url_for("main.games_list"))

@main_bp.route("/standings")
def standings():
    players = Player.query.all()

    standings_data = []
    for player in players:
        games_played = Game.query.filter(
            (Game.player1_id == player.id) |
            (Game.player2_id == player.id) |
            (Game.player3_id == player.id) |
            (Game.player4_id == player.id)
        ).all()

        wins = 0
        losses = 0
        wins_right = 0
        wins_left = 0
        losses_right = 0
        losses_left = 0
        points_made = 0
        points_received = 0

        for game in games_played:
            if game.player1_id == player.id:
                if game.score_team1 > game.score_team2:
                    wins += 1
                    wins_right += 1
                else:
                    losses += 1
                    losses_right += 1
                points_made += game.score_team1
                points_received += game.score_team2

            elif game.player2_id == player.id:
                if game.score_team1 > game.score_team2:
                    wins += 1
                    wins_left += 1
                else:
                    losses += 1
                    losses_left += 1
                points_made += game.score_team1
                points_received += game.score_team2

            elif game.player3_id == player.id:
                if game.score_team2 > game.score_team1:
                    wins += 1
                    wins_right += 1
                else:
                    losses += 1
                    losses_right += 1
                points_made += game.score_team2
                points_received += game.score_team1

            elif game.player4_id == player.id:
                if game.score_team2 > game.score_team1:
                    wins += 1
                    wins_left += 1
                else:
                    losses += 1
                    losses_left += 1
                points_made += game.score_team2
                points_received += game.score_team1

        diff = points_made - points_received

        standings_data.append({
            "name": player.name,
            "wins": wins,
            "losses": losses,
            "wins_right": wins_right,
            "losses_right": losses_right,
            "wins_left": wins_left,
            "losses_left": losses_left,
            "points_made": points_made,
            "points_received": points_received,
            "diff": diff
        })

    standings_data.sort(key=lambda x: (-x["wins"], -x["diff"], -x["points_made"]))

    return render_template("standings.html", standings=standings_data)

@main_bp.route("/schuldenberger")
def schuldenberger():
    COST_PER_POINT = 0.50  # Cost per point difference, easily adjustable

    players = Player.query.all()
    games = Game.query.all()

    # Initialize a debt dictionary for each player
    schulden_data = {
        player.id: {"name": player.name, "debt": 0.0, "loss_points_diff": 0} for player in players
    }

    # Calculate debt per player based on individual participation
    for game in games:
        point_difference = abs(game.score_team1 - game.score_team2)

        if game.score_team1 > game.score_team2:
            # Team 2 loses; calculate debt and loss points diff for Player 3 and Player 4
            schulden_data[game.player3_id]["debt"] += point_difference * COST_PER_POINT
            schulden_data[game.player4_id]["debt"] += point_difference * COST_PER_POINT
            schulden_data[game.player3_id]["loss_points_diff"] += point_difference
            schulden_data[game.player4_id]["loss_points_diff"] += point_difference
        elif game.score_team2 > game.score_team1:
            # Team 1 loses; calculate debt and loss points diff for Player 1 and Player 2
            schulden_data[game.player1_id]["debt"] += point_difference * COST_PER_POINT
            schulden_data[game.player2_id]["debt"] += point_difference * COST_PER_POINT
            schulden_data[game.player1_id]["loss_points_diff"] += point_difference
            schulden_data[game.player2_id]["loss_points_diff"] += point_difference

    # Convert debt dictionary into a list for easier rendering
    schulden_list = [
        {
            "name": data["name"],
            "debt": round(data["debt"], 2),
            "loss_points_diff": data["loss_points_diff"],
        }
        for data in schulden_data.values()
    ]
    total_debt = sum(data["debt"] for data in schulden_data.values())

    return render_template(
        "schuldenberger.html",
        schulden_data=schulden_list,
        total_debt=round(total_debt, 2),
    )

