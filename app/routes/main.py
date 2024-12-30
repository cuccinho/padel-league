from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models import Player, Game, AmericanoPlayer, AmericanoGame, AmericanoTournament
from app.extensions import db
from datetime import datetime
from itertools import combinations, permutations
import random
from math import ceil

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


@main_bp.route("/players/add", methods=["GET", "POST"])
def add_player():
    if request.method == "POST":
        player_name = request.form.get("name")
        if not player_name:
            flash("Player name is required.", "danger")
            return render_template("add_player.html")

        # Check if the player already exists
        existing_player = Player.query.filter_by(name=player_name).first()
        if existing_player:
            flash("Player already exists.", "danger")
            return render_template("add_player.html")

        # Add new player
        new_player = Player(name=player_name)
        db.session.add(new_player)
        db.session.commit()
        flash(f"Player '{player_name}' added successfully!", "success")
        return redirect(url_for("main.players_list"))

    return render_template("add_player.html")


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
        match_date = request.form.get("match_date")

        # Set default date to today if not provided
        try:
            match_date = datetime.strptime(match_date, "%Y-%m-%d") if match_date else datetime.utcnow()
        except ValueError:
            return render_template("add_game.html", players=players, error="Invalid date format. Please try again.")

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
            date=match_date  # Store the selected match date here
        )
        db.session.add(new_game)
        db.session.commit()

        # Pass success message directly to the template
        return render_template(
            "games_list.html",
            games=Game.query.order_by(Game.date.desc()).all(),  # Order by date for clarity
            players=Player.query.all(),
            success="Game added successfully."
        )

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
            schulden_data[game.player3_id]["debt"] += point_difference * COST_PER_POINT
            schulden_data[game.player4_id]["debt"] += point_difference * COST_PER_POINT
            schulden_data[game.player3_id]["loss_points_diff"] += point_difference
            schulden_data[game.player4_id]["loss_points_diff"] += point_difference
        elif game.score_team2 > game.score_team1:
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
        cost_per_point=COST_PER_POINT  # Pass cost per point to the template
    )

@main_bp.route('/get_player_combination_stats')
def get_player_combination_stats():
    player1 = request.args.get('player1')
    player2 = request.args.get('player2')

    if not player1 or not player2:
        return jsonify({'error': 'Both players must be selected'}), 400

    # Filter games based on the selected players and positions
    games = Game.query.all()
    wins, losses = 0, 0

    for game in games:
        team1 = [
            f"{game.player1.name} ({game.position1})",
            f"{game.player2.name} ({game.position2})",
        ]
        team2 = [
            f"{game.player3.name} ({game.position3})",
            f"{game.player4.name} ({game.position4})",
        ]

        if player1 in team1 and player2 in team1:
            if game.score_team1 > game.score_team2:
                wins += 1
            else:
                losses += 1
        elif player1 in team2 and player2 in team2:
            if game.score_team2 > game.score_team1:
                wins += 1
            else:
                losses += 1

    return jsonify({'wins': wins, 'losses': losses})


@main_bp.route("/games/delete/<int:game_id>", methods=["POST"])
def delete_game(game_id):
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
    return redirect(url_for("main.games_list"))

@main_bp.route("/americano", methods=["GET", "POST"])
def americano():
    tournaments = AmericanoTournament.query.all()
    return render_template("americano.html", tournaments=tournaments)

@main_bp.route("/americano/create", methods=["GET", "POST"])
def create_tournament():
    if request.method == "POST":
        tournament_name = request.form["tournament_name"]
        num_courts = int(request.form["num_courts"])
        player_names = request.form.getlist("player_names")

        if len(player_names) < 4:
            flash("At least 4 players are required to create a tournament.", "danger")
            return redirect(url_for("main.create_tournament"))

        tournament = AmericanoTournament(name=tournament_name, num_courts=num_courts)
        db.session.add(tournament)
        db.session.flush()  # Get the ID of the new tournament

        players = []
        for name in player_names:
            player = AmericanoPlayer(name=name, tournament_id=tournament.id)
            db.session.add(player)
            db.session.flush()
            players.append(player)

        generate_americano_matches(players, tournament.id, num_courts)
        db.session.commit()

        flash(f"Tournament '{tournament_name}' created successfully!", "success")
        return redirect(url_for("main.americano"))

    return render_template("create_tournament.html")


def generate_americano_matches(players, tournament_id, num_courts):
    from itertools import permutations
    import random

    num_players = len(players)
    num_rounds = num_players - 1  # For a round-robin tournament
    matches_per_round = num_courts  # Matches per round (2 matches for 8 players)

    # Create a randomized pool of players
    random.shuffle(players)

    # Keep track of which players have already been paired
    used_pairings = set()
    matches = []

    for round_number in range(1, num_rounds + 1):
        round_matches = []
        round_used_players = set()

        for match_number in range(matches_per_round):
            pair1, pair2 = None, None

            # Find two pairs of players that satisfy the conditions
            for player1 in players:
                if player1 in round_used_players:
                    continue

                for player2 in players:
                    if player2 in round_used_players or player2 == player1:
                        continue

                    if frozenset([player1, player2]) not in used_pairings:
                        pair1 = (player1, player2)
                        break
                if pair1:
                    break

            for player3 in players:
                if player3 in round_used_players or player3 in pair1:
                    continue

                for player4 in players:
                    if (
                            player4 in round_used_players
                            or player4 in pair1
                            or player4 == player3
                    ):
                        continue

                    if frozenset([player3, player4]) not in used_pairings:
                        pair2 = (player3, player4)
                        break
                if pair2:
                    break

            # If valid pairs are found, assign them to the match
            if pair1 and pair2:
                round_matches.append((pair1, pair2))
                round_used_players.update(pair1)
                round_used_players.update(pair2)

                # Mark pairs as used
                used_pairings.add(frozenset(pair1))
                used_pairings.add(frozenset(pair2))

        # Save the matches to the database
        for match in round_matches:
            (player1, player2), (player3, player4) = match
            game = AmericanoGame(
                player1_id=player1.id,
                player2_id=player2.id,
                player3_id=player3.id,
                player4_id=player4.id,
                tournament_id=tournament_id,
            )
            db.session.add(game)
            matches.append(game)

    db.session.commit()


@main_bp.route("/americano/tournament/<int:tournament_id>")
def view_tournament(tournament_id):
    tournament = AmericanoTournament.query.get(tournament_id)
    if not tournament:
        flash("Tournament not found.", "danger")
        return redirect(url_for("main.americano"))

    matches = AmericanoGame.query.filter_by(tournament_id=tournament_id).all()
    matches_by_round = {}
    for idx, game in enumerate(matches, start=1):
        round_number = ceil(idx / tournament.num_courts)
        if round_number not in matches_by_round:
            matches_by_round[round_number] = []
        matches_by_round[round_number].append(game)

    leaderboard = calculate_americano_table(tournament_id)
    return render_template(
        "tournament_view.html",
        tournament=tournament,
        matches_by_round=matches_by_round,
        leaderboard=leaderboard,
    )

@main_bp.route("/americano/update/<int:game_id>", methods=["POST"])
def update_americano_game(game_id):
    game = AmericanoGame.query.get(game_id)
    if not game:
        flash("Match not found.", "danger")
        return redirect(request.referrer or url_for("main.americano"))

    score_team1 = request.form.get("score_team1")
    score_team2 = request.form.get("score_team2")

    if score_team1.isdigit() and score_team2.isdigit():
        game.score_team1 = int(score_team1)
        game.score_team2 = int(score_team2)
        db.session.commit()
        flash("Match result updated successfully!", "success")
    else:
        flash("Invalid scores entered!", "danger")

    return redirect(request.referrer or url_for("main.view_tournament", tournament_id=game.tournament_id))

def calculate_americano_table(tournament_id):
    players = AmericanoPlayer.query.filter_by(tournament_id=tournament_id).all()
    results = {player.id: {
        "name": player.name,
        "points": 0,
        "matches_played": 0,
        "wins": 0,
        "losses": 0,
        "points_scored": 0,
        "points_against": 0
    } for player in players}

    games = AmericanoGame.query.filter_by(tournament_id=tournament_id).all()
    for game in games:
        if game.score_team1 is not None and game.score_team2 is not None:
            # Update points
            if game.score_team1 > game.score_team2:
                results[game.player1_id]["points"] += 3
                results[game.player2_id]["points"] += 3
                results[game.player3_id]["losses"] += 1
                results[game.player4_id]["losses"] += 1
            elif game.score_team2 > game.score_team1:
                results[game.player3_id]["points"] += 3
                results[game.player4_id]["points"] += 3
                results[game.player1_id]["losses"] += 1
                results[game.player2_id]["losses"] += 1

            # Update stats for matches played, points scored, and points against
            results[game.player1_id]["points_scored"] += game.score_team1
            results[game.player2_id]["points_scored"] += game.score_team1
            results[game.player3_id]["points_scored"] += game.score_team2
            results[game.player4_id]["points_scored"] += game.score_team2

            results[game.player1_id]["points_against"] += game.score_team2
            results[game.player2_id]["points_against"] += game.score_team2
            results[game.player3_id]["points_against"] += game.score_team1
            results[game.player4_id]["points_against"] += game.score_team1

            results[game.player1_id]["matches_played"] += 1
            results[game.player2_id]["matches_played"] += 1
            results[game.player3_id]["matches_played"] += 1
            results[game.player4_id]["matches_played"] += 1

            if game.score_team1 > game.score_team2:
                results[game.player1_id]["wins"] += 1
                results[game.player2_id]["wins"] += 1
            else:
                results[game.player3_id]["wins"] += 1
                results[game.player4_id]["wins"] += 1

    # Sort results: by points, then by points scored, then by point difference
    return sorted(
        results.values(),
        key=lambda x: (-x["points"], -x["points_scored"], -(x["points_scored"] - x["points_against"]))
    )

@main_bp.route("/americano/leaderboard/<int:tournament_id>")
def leaderboard(tournament_id):
    tournament = AmericanoTournament.query.get(tournament_id)
    if not tournament:
        flash("Tournament not found.", "danger")
        return redirect(url_for("main.americano"))

    leaderboard = calculate_americano_table(tournament_id)
    return render_template("leaderboard.html", tournament=tournament, leaderboard=leaderboard)


