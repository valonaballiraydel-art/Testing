from flask import Flask, request, jsonify
from scraper import scrape_standings

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "ok", "message": "SofaScore Scraper running"}

@app.route("/scrape")
def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing url parameter"}), 400

    data = scrape_standings(url)
    return jsonify({"standings": data})

if __name__ == "__main__":
    app.run()
