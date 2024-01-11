import datetime
import requests
import pandas as pd
import Player

def makeGuess():
    # get list of all teams playing
    target_date = datetime.date.today().strftime('%Y-%m-%d')
    URL = "https://api-web.nhle.com/v1/schedule/now"
    r = requests.get(URL)
    data = r.json()
    teams = []
    teamABBR = []

    for game_day in data["gameWeek"]:
        if game_day["date"] == target_date:
            for game in game_day["games"]:
                teams.append(game["awayTeam"]["placeName"]["default"])
                teamABBR.append(game["awayTeam"]["abbrev"])
                teams.append(game["homeTeam"]["placeName"]["default"])
                teamABBR.append(game["homeTeam"]["abbrev"])

    allPlayers = []
    for i in range(0, len(teamABBR)):
        fullUrl = f"https://api-web.nhle.com/v1/roster/{teamABBR[i]}/20232024"
        print(f"Loading roster for {teams[i]}")

        response = requests.get(fullUrl)
        data = response.json()

        for player in data['forwards']:
            allPlayers.append({
                "firstName": player['firstName']['default'], 
                "lastName": player['lastName']['default'],
                "id": player['id']})

    for player in allPlayers:
        p = Player.Player(player['firstName'], player['lastName'], player['id'])
        print(f"{p.getName}, {p.getStat()}")
        

makeGuess()