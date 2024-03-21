import datetime
from itertools import chain
from multiprocessing import Pool
import requests

import Player
from newDataHandler import updateGoalScorerRows

filename = "D:\\code\\python\\tims-picker\\lib\\data.csv"

def get_players(game_data):
    players = []
    
    # Extract players from both away and home teams
    for team in ['awayTeam', 'homeTeam']:
        for player_type in ['forwards', 'defense']:
            for player in game_data[team][player_type]:
                player_info = {
                    'playerId': player['playerId'],
                    'name': player['name']['default'],
                    'toi': player['toi'],
                    'goals': player['goals']
                }
                players.append(player_info)
    
    return players

def updateScored():
    # get goal scorers
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    date = yesterday.strftime('%Y-%m-%d')

    url = f"https://api-web.nhle.com/v1/score/{date}"
    r = requests.get(url)
    json_data = r.json()

    playersWhoPlayed = []
    # Parse through each game
    for game in json_data['games']:
        # Parse through each goal in the game
        url = f"https://api-web.nhle.com/v1/gamecenter/{game['id']}/boxscore"
        r = requests.get(url)
        newData = r.json()

        # get players from both home and away teams
        playersWhoPlayed += get_players(newData['playerByGameStats'])

    # we now have all players who played
    updateGoalScorerRows(filename, date, playersWhoPlayed)

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

def getRoster(teamABBR):
    players = []

    URL = f"https://api-web.nhle.com/v1/roster/{teamABBR}/20232024"
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

def getPlayersFromTeam(team):
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

    # utilize multiprocessing pool to get all players from each team (use each team as a thread)
    with Pool() as pool:
        result_lists = pool.map(getPlayersFromTeam, teams)
        allPlayers.extend(chain.from_iterable(result_lists))

    return allPlayers

def getAllPlayers():
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

def main():
    updateScored()

    # get all players today
    players = getAllPlayers()
    # get odds and link them

if __name__ == "__main__":
    main()
