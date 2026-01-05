from flask import Flask, request, jsonify
import traceback
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
        # Added traceback to help you debug the exact failure point
        return jsonify({
            "error": "Failed to fetch standings",
            "details": str(e),
            "traceback": traceback.format_exc()
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
