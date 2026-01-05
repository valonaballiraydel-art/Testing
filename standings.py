import os
import time
import requests

# This must match the variable name in your Render Dashboard
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BASE_URL = "https://api.football-data.org/v4/competitions"

CACHE = {}
CACHE_TTL = 900  # 15 minutes (Free tier limit is 10 calls/min)

# League codes specifically for Football-Data.org
LEAGUE_CODES = {
    "england": "PL",   # Premier League
    "spain": "PD"      # Primera Division (La Liga)
}

def get_standings(league_key, season=None):
    if league_key not in LEAGUE_CODES:
        raise ValueError(f"League '{league_key}' not supported. Use 'england' or 'spain'.")

    # The API defaults to the current season if none is provided
    cache_key = f"{league_key}_{season or 'current'}"
    now = time.time()

    if cache_key in CACHE and now - CACHE[cache_key]["time"] < CACHE_TTL:
        return CACHE[cache_key]["data"]

    league_code = LEAGUE_CODES[league_key]
    url = f"{BASE_URL}/{league_code}/standings"
    
    # Football-Data.org requires 'X-Auth-Token' in the header
    headers = { 'X-Auth-Token': API_KEY }
    params = {}
    if season:
        params['season'] = season

    response = requests.get(url, headers=headers, params=params, timeout=20)
    
    if response.status_code == 403:
        raise Exception("Access Denied: Check your API key or league permissions.")
    
    response.raise_for_status()
    data = response.json()

    # Access the 'TOTAL' standings table from the results
    standings_list = data.get("standings", [])
    if not standings_list:
        raise ValueError("No standings data found.")

    total_table = next((s for s in standings_list if s.get('type') == 'TOTAL'), standings_list[0])
    rows = total_table.get("table", [])

    formatted_standings = []
    for row in rows:
        formatted_standings.append({
            "position": row.get("position"),
            "team": row.get("team", {}).get("name"),
            "played": row.get("playedGames"),
            "wins": row.get("won"),
            "draws": row.get("draw"),
            "losses": row.get("lost"),
            "points": row.get("points"),
            "goal_diff": row.get("goalDifference")
        })

    result = {
        "league": data.get("competition", {}).get("name"),
        "season": data.get("filters", {}).get("season"),
        "standings": formatted_standings
    }

    CACHE[cache_key] = {"time": now, "data": result}
    return result
