import os
import time
import requests

API_KEY = os.getenv("ALLSPORTS_API_KEY")
BASE_URL = "https://apiv2.allsportsapi.com/football"

# Cache (league + season)
CACHE = {}
CACHE_TTL = 300  # 5 minutes

LEAGUES = {
    "england": {
        "country_id": 44,
        "league_name": "Premier League"
    },
    "spain": {
        "country_id": 6,
        "league_name": "La Liga"
    }
}

def get_league_id(country_id, league_name):
    params = {
        "met": "Leagues",
        "countryId": country_id,
        "APIkey": API_KEY
    }

    res = requests.get(BASE_URL, params=params, timeout=20)
    res.raise_for_status()

    leagues = res.json()["result"]

    for league in leagues:
        if league_name.lower() in league["league_name"].lower():
            return league["league_key"]

    raise ValueError("League not found")

def get_standings(league_key, season=None):
    if league_key not in LEAGUES:
        raise ValueError("Unsupported league")

    season = season or "current"
    cache_key = f"{league_key}_{season}"
    now = time.time()

    if cache_key in CACHE and now - CACHE[cache_key]["time"] < CACHE_TTL:
        return CACHE[cache_key]["data"]

    league = LEAGUES[league_key]
    league_id = get_league_id(league["country_id"], league["league_name"])

    params = {
        "met": "Standings",
        "leagueId": league_id,
        "APIkey": API_KEY
    }

    if season != "current":
        params["season"] = season

    res = requests.get(BASE_URL, params=params, timeout=20)
    res.raise_for_status()

    payload = res.json()

    # 🔒 SAFETY CHECKS
    if "result" not in payload or not payload["result"]:
        raise ValueError("No standings data returned")

    standings_block = payload["result"][0]

    if "standings" not in standings_block:
        raise ValueError("Standings field missing in API response")

    teams = standings_block["standings"]

    standings = []
    for team in teams:
        standings.append({
            "position": int(team["overall_league_position"]),
            "team": team["team_name"],
            "played": int(team["overall_league_payed"]),
            "wins": int(team["overall_league_W"]),
            "draws": int(team["overall_league_D"]),
            "losses": int(team["overall_league_L"]),
            "goals_for": int(team["overall_league_GF"]),
            "goals_against": int(team["overall_league_GA"]),
            "goal_diff": int(team["overall_league_GF"]) - int(team["overall_league_GA"]),
            "points": int(team["overall_league_PTS"])
        })

    data = {
        "league": league["league_name"],
        "season": season,
        "standings": standings
    }

    CACHE[cache_key] = {"time": now, "data": data}
    return data
