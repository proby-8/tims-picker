import datetime
from itertools import chain
import time
import requests
from multiprocessing import Pool

import Player

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

def getTeams(data, target_date):
    teams = []

    for game_day in data["gameWeek"]:
        if game_day["date"] == target_date:
            for game in game_day["games"]:
                teamInfoHome = {
                    'name': (game["homeTeam"]["placeName"]["default"]),
                    'abbr': (game["homeTeam"]["abbrev"]),
                    'id': (game['homeTeam']['id']),
                    'otherId': (game['awayTeam']['id']),
                    'home': 1
                }
                teamInfoAway = {
                    'name': (game["awayTeam"]["placeName"]["default"]),
                    'abbr': (game["awayTeam"]["abbrev"]),
                    'id': (game['awayTeam']['id']),
                    'otherId': (game['homeTeam']['id']),
                    'home': 0
                }

                teams.append(teamInfoHome)
                teams.append(teamInfoAway)

    return teams

def getPlayersFromTeam(team):
    Player.Player.initTeamStats(team['id'], team['otherId'])
    allPlayers = []

    roster = getRoster(team['abbr'])
    print(f"Gathering stats for team {team['name']}")

    url = f"https://api-web.nhle.com/v1/club-stats/{team['abbr']}/20232024/2"
    r = requests.get(url)
    data = r.json()    

    for player in roster:
        allPlayers.append(Player.Player(player['name'], player['id'], team['name'], team['abbr'], team['id'], team['otherId'], team['home'], data))

    return allPlayers


def getPlayers(teams):
    allPlayers = []

    with Pool() as pool:
        result_lists = pool.map(getPlayersFromTeam, teams)
        allPlayers.extend(chain.from_iterable(result_lists))

    return allPlayers

def getAllPlayers():
    # currently testing during all-star week
    # target_date = "2024-01-26"
    target_date = datetime.date.today().strftime('%Y-%m-%d')

    URL = f"https://api-web.nhle.com/v1/schedule/{target_date}"

    r = requests.get(URL)
    data = r.json()

    teams = getTeams(data, target_date)

    print("Teams playing today:")
    for team in teams:
        print(f"\t{team['name']}")
    print("")

    allPlayers = getPlayers(teams)

    return allPlayers


def rank():
    allPlayers = getAllPlayers()
    allPlayers = sorted(allPlayers, reverse=True)

    Player.Player.printHeader()
    for player in allPlayers:
        print(f"\t{player}")

if __name__ == "__main__":
    rank()