import requests

def scrape_standings(url=None):
    api_url = "https://api.sofascore.com/api/v1/unique-tournament/17/season/52186/standings/total"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    r = requests.get(api_url, headers=headers, timeout=20)
    r.raise_for_status()

    data = r.json()

    standings = []

    for row in data["standings"][0]["rows"]:
        standings.append({
            "position": row["position"],
            "team": row["team"]["name"],
            "played": row["matches"],
            "points": row["points"]
        })

    return {
        "league": "Premier League",
        "season": "2025/26",
        "standings": standings
    }
