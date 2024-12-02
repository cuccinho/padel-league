from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Player
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
