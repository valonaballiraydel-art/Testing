import requests

SOFASCORE_API = "https://api.sofascore.com/api/v1"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def scrape_standings(tournament_id, season_id):
    url = f"{SOFASCORE_API}/unique-tournament/{tournament_id}/season/{season_id}/standings/total"

    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    data = response.json()

    if "standings" not in data or not data["standings"]:
        return []

    rows = data["standings"][0].get("rows", [])
    standings = []

    for row in rows:
        standings.append({
            "position": row.get("position"),
            "team": row["team"]["name"],
            "played": row.get("matches"),
            "wins": row.get("wins"),
            "draws": row.get("draws"),
            "losses": row.get("losses"),
            "goals_for": row.get("scoresFor"),
            "goals_against": row.get("scoresAgainst"),
            "goal_diff": row.get("goalDiff"),
            "points": row.get("points")
        })

    return standings
