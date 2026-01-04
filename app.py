from flask import Flask, request, jsonify
from scraper import scrape_standings

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "SofaScore Football Standings API"
    })

@app.route("/standings")
def standings():
    tournament_id = request.args.get("tournament_id")
    season_id = request.args.get("season_id")

    if not tournament_id or not season_id:
        return jsonify({
            "error": "Missing tournament_id or season_id"
        }), 400

    data = scrape_standings(tournament_id, season_id)

    return jsonify({
        "tournament_id": tournament_id,
        "season_id": season_id,
        "standings": data
    })
