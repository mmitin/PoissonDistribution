# takes the matches from the current LaLiga round

import requests
import json

# API key from football-data.org
API_KEY = "196f59f9510c405489824632e5a36ecc"

# Settings
SEASON = 2025   
ROUND = 11      # round number

# request to the official API
url = f"https://api.football-data.org/v4/competitions/PD/matches?season={SEASON}"
headers = {"X-Auth-Token": API_KEY}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    print(response.text)
    exit()

data = response.json()


# gets the matches from the upcomming round
def matchGetter():
    matches = []
    for m in data["matches"]:
        if m["matchday"] == ROUND:
            match = {
                "homeTeam": m["homeTeam"]["name"],
                "awayTeam": m["awayTeam"]["name"],
            }
            matches.append(match)
    createJSONFile(matches, fileName ='matchDayList')

# gets the results from the previus round
def resultsGetter():
    matches = []
    for m in data["matches"]:
        if m["matchday"] == ROUND:
            match = {
                "homeTeam": m["homeTeam"]["name"],
                "homeGoalsScored": m["score"]["fullTime"]['home'],
                "awayTeam": m["awayTeam"]["name"],
                "awayGoalsScored": m["score"]["fullTime"]['away']
            }
            matches.append(match)
    createJSONFile(matches, fileName ='matchDayResults')

# creates JSON file
def createJSONFile(matches, fileName):
    json_filename = f"jsonFiles/{fileName}.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)

    print(f"✅ Извлечени {len(matches)} мача от кръг {ROUND} ({SEASON})")
    print(f"📁 Записани в: {json_filename}")

