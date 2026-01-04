import requests

def scrape_standings(tournament_id, season_id):
    api_url = f"https://api.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/standings/total"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    response = requests.get(api_url, headers=headers, timeout=20)
    response.raise_for_status()

    data = response.json()

    standings = []

    # SofaScore returns multiple standings types (total/home/away)
    for row in data["standings"][0]["rows"]:
        standings.append({
            "position": row["position"],
            "team": row["team"]["name"],
            "played": row["matches"],
            "wins": row["wins"],
            "draws": row["draws"],
            "losses": row["losses"],
            "goals_for": row["scoresFor"],
            "goals_against": row["scoresAgainst"],
            "goal_diff": row["goalDiff"],
            "points": row["points"]
        })

    return standings
