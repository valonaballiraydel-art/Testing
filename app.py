from flask import Flask, request, jsonify
from standings import get_standings

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Football Standings API (England & Spain)"
    })

@app.route("/standings")
def standings():
    league = request.args.get("league")
    season = request.args.get("season")  # optional

    if not league:
        return jsonify({"error": "Missing league parameter"}), 400

    try:
        data = get_standings(league.lower(), season)
        return jsonify(data)
    except Exception as e:
        return jsonify({
            "error": "Failed to fetch standings",
            "details": str(e)
        }), 500
