import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

API_KEY = os.environ.get("FOOTBALL_API_KEY")

LEAGUES = {
    "premier-league": "PL",
    "la-liga": "PD",
    "serie-a": "SA",
    "bundesliga": "BL1",
    "ligue-1": "FL1",
    "brasileirao": "BSA"
}

@app.route("/")
def home():
    return {"status": "ok", "message": "Football Standings API"}

@app.route("/standings/<league>")
def standings(league):
    if league not in LEAGUES:
        return jsonify({"error": "League not supported"}), 400

    code = LEAGUES[league]
    url = f"https://api.football-data.org/v4/competitions/{code}/standings"

    headers = {
        "X-Auth-Token": API_KEY
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return jsonify({"error": "API error"}), 500

    data = r.json()
    table = data["standings"][0]["table"]

    standings = []
    for team in table:
        standings.append({
            "position": team["position"],
            "team": team["team"]["name"],
            "played": team["playedGames"],
            "points": team["points"],
            "goal_difference": team["goalDifference"]
        })

    return jsonify({
        "league": league,
        "standings": standings
    })

if __name__ == "__main__":
    app.run()
