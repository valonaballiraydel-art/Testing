from flask import Flask, request, jsonify
import traceback
from standings import get_standings

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Football Standings API via Football-Data.org"
    })

@app.route("/standings")
def standings():
    league = request.args.get("league")
    season = request.args.get("season") 

    if not league:
        return jsonify({"error": "Missing league parameter"}), 400

    try:
        data = get_standings(league.lower(), season)
        return jsonify(data)
    except Exception as e:
        return jsonify({
            "error": "Standings Lookup Failed",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

import os
import requests

API_KEY = os.getenv("FOOTBALL_API_KEY")

@app.route("/standings")
def standings():
    url = "https://api.football-data.org/v4/competitions/PL/standings"
    headers = {"X-Auth-Token": API_KEY}

    r = requests.get(url, headers=headers)
    data = r.json()

    return jsonify(data)

@app.route("/test-key")
def test_key():
    return jsonify({"key_loaded": bool(API_KEY)})


