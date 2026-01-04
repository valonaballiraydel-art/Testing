import requests

SOFASCORE_API = "https://api.sofascore.com/api/v1"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.sofascore.com/",
    "Origin": "https://www.sofascore.com"
}

def scrape_standings(tournament_id, season_id):
    url = f"{SOFASCORE_API}/unique-tournament/{tournament_id}/season/{season_id}/standings/total"

    response = requests.get(url, headers=HEADERS, timeout=20)

    if response.status_code == 403:
        raise Exception("Blocked by SofaScore (403). Headers rejected.")

    response.raise_for_status()
    data = response.json()

    standings = []

    if "standings" not in data or not data["standings"]:
        return standings

    rows = data["standings"][0].get("rows", [])

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
