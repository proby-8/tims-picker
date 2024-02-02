import datetime
import requests

import NewPlayer

def getRoster(teamABBR):
    URL = f"https://api-web.nhle.com/v1/roster/{teamABBR}/20232024"

    players = []
    r = requests.get(URL)
    data = r.json()

    forwards = data['forwards']
    defense = data['defensemen']
    # goalies = data['goalies']

    for f in forwards:
        player_info = {
            'name': f['firstName']['default'] + " " + f['lastName']['default'],
            'id': f['id']
        }
        players.append(player_info)

    for d in defense:
        player_info = {
            'name': d['firstName']['default'] + " " + d['lastName']['default'],
            'id': d['id']
        }
        players.append(player_info)

    return players

def makeGuess():
    # get list of all teams playing

    # currently testing during all-star week
    #target_date = datetime.date.today().strftime('%Y-%m-%d')
    target_date = "2024-01-26"

    URL = f"https://api-web.nhle.com/v1/schedule/{target_date}"

    r = requests.get(URL)
    data = r.json()
    teams = []

    for game_day in data["gameWeek"]:
        if game_day["date"] == target_date:
            for game in game_day["games"]:
                teamInfoHome = {
                    'name': (game["homeTeam"]["placeName"]["default"]),
                    'abbr': (game["homeTeam"]["abbrev"])
                }
                teamInfoAway = {
                    'name': (game["awayTeam"]["placeName"]["default"]),
                    'abbr': (game["awayTeam"]["abbrev"])
                }

                teams.append(teamInfoHome)
                teams.append(teamInfoAway)

    teams=[{
        'name': "Dont care",
        "abbr": "TOR"
    }]

    print("Teams playing today:")
    for team in teams:
        print(f"\t{team['name']}")
    print("")

    allPlayers = []

    for team in teams:
        roster = getRoster(team['abbr'])
        print(f"Gathering stats for team {team['name']}")

        for player in roster:
            allPlayers.append(NewPlayer.Player(player['name'], player['id']))

    allPlayers = sorted(allPlayers, reverse=True)

    print("Players in order:")
    for player in allPlayers:
        print(f"\t{player}")

makeGuess()