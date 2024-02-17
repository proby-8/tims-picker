import datetime
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
            # Read the first line to check the date
            first_line = file.readline().strip().split(',')[0]
            # Check if the date matches the current date
            if first_line != currentDate:
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


def linker(players, playerInfo):
    for player in playerInfo:
        matchFound = 0
        # could change to sort and binary search, but only takes 0.00001 seconds anyways
        for playerData in players:
            if player['name'] == playerData.getName():
                matchFound = 1
                playerData.setBet(player['bet'])
        
        if (not matchFound):
            print(f"Could not find - Player: {player['name']}, Bet: {player['bet']}")


def getGoalScorers(date):
    url = f"https://api-web.nhle.com/v1/score/{date}"

    r = requests.get(url)
    json_data = r.json()

    goalScorers = []
    
    # Parse through each game
    for game in json_data['games']:
        # Parse through each goal in the game
        for goal in game['goals']:
            scorer_info = {
                'player_id': goal['playerId'],
                'player_name': goal['name']['default'],
                'team_abbrev': goal['teamAbbrev'],
                'time': goal['timeInPeriod'],
                'period': goal['period'],
                'strength': goal['strength']
            }
            goalScorers.append(scorer_info)

    return goalScorers


def inList(id, listIds):
    for lId in listIds:
        if str(id) == str(lId):
            return True
    
    return False

def updateGoalScorers():

    print("\nUpdating goal scorers")

    # get yesterday
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    date = yesterday.strftime('%Y-%m-%d')

    goalScorers = getGoalScorers(date)

    player_ids = [player['player_id'] for player in goalScorers]

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
                    if (row[1] not in {0,1}):
                        # Check if player scored
                        if (inList(row[3], player_ids)):
                            row[1] = '1'
                        else:
                            row[1] = '0'
                writer.writerow(row)
