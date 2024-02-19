import datetime
import json
import os
import requests
import csv

import Player
import allPlayers
import oddsScraper

def main():
    save()
    updateGoalScorers()

def save():

    players = allPlayers.getAllPlayers()

    playerInfo = oddsScraper.scraper()

    linker(players, playerInfo)

    currentDate = datetime.datetime.now().strftime('%Y-%m-%d')

    # Check if the file exists
    if os.path.isfile('lib/data.csv'):
        with open('lib/data.csv', 'r') as file:
            lines = file.readlines()
            last_line = lines[-1].strip().split(',')[0]

            if last_line != currentDate:
                print("Writing")
                with open('lib/data.csv', 'a') as fd:
                    for player in players:
                        fd.write(f"{currentDate},")
                        fd.write(player.toCSV())
    else:
        # If the file doesn't exist, create it and write the current date and player information
        with open('lib/data.csv', 'a') as fd:
            fd.write(Player.Player.headerToCSV())
            for player in players:
                fd.write(f"{currentDate},")
                fd.write(player.toCSV())


def compareNames(name1, name2):
    name1 = str(name1).lower().replace(" ", "")
    name2 = str(name2).lower().replace(" ", "")

    if name1 == name2:
        return True
    return False


def linker(players, playerInfo):
    for player in playerInfo:
        matchFound = 0
        # could change to sort and binary search, but only takes 0.00001 seconds anyways
        for playerData in players:
            if compareNames(player['name'], playerData.getName()):
                matchFound = 1
                playerData.setBet(player['bet'])
        
        if (not matchFound):
            print(f"Could not find - Player: {player['name']}, Bet: {player['bet']}")


def get_players(game_data):
    players = []
    
    # Extract players from both away and home teams
    for team in ['awayTeam', 'homeTeam']:
        for player_type in ['forwards', 'defense']:
            for player in game_data['playerByGameStats'][team][player_type]:
                player_info = {
                    'playerId': player['playerId'],
                    'name': player['name']['default'],
                    'toi': player['toi'],
                    'goals': player['goals']
                }
                players.append(player_info)
    
    return players


def getGoalScorers(date):
    url = f"https://api-web.nhle.com/v1/score/{date}"

    r = requests.get(url)
    json_data = r.json()

    # goalScorers = []
    playersWhoPlayed = []
    
    # Parse through each game
    for game in json_data['games']:
        # Parse through each goal in the game
        url = f"https://api-web.nhle.com/v1/gamecenter/{game['id']}/boxscore"
        r = requests.get(url)
        newData = r.json()

        playersWhoPlayed += get_players(newData['boxscore'])

        # for goal in game['goals']:
        #     scorer_info = {
        #         'player_id': goal['playerId'],
        #         'player_name': goal['name']['default'],
        #         'team_abbrev': goal['teamAbbrev'],
        #         'time': goal['timeInPeriod'],
        #         'period': goal['period'],
        #         'strength': goal['strength']
        #     }
        #     goalScorers.append(scorer_info)

    return playersWhoPlayed


def inList(id, listIds):
    for lId in listIds:
        if str(id) == str(lId):
            return True
    
    return False

def findMatch(id, players):
    matching_player = None
    for player in players:
        if str(player['playerId']) == str(id):
            matching_player = player
            break  # Stop the loop once a match is found

    return matching_player

def updateGoalScorers():

    print("\nUpdating goal scorers")

    # get yesterday
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    date = yesterday.strftime('%Y-%m-%d')

    playersWhoPlayed = getGoalScorers(date)

    if os.path.isfile('lib/data.csv'):
        with open('lib/data.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header line
            rows = list(reader)  # Read the remaining rows into a list of lists

        with open('lib/data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write back the header line
            
            for row in rows:
                if row[0] == date:

                    # for each row in correct date
                    match = findMatch(row[3], playersWhoPlayed)

                    # if not match, remove from csv as they did not play
                    if match:
                        if (row[1] not in {0,1}):
                            # Check if player scored

                            if (match['goals'] > 0):
                                row[1] = '1'
                            else:
                                row[1] = '0'
                        writer.writerow(row)
                 
                else:
                    writer.writerow(row)

updateGoalScorers()