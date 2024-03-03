import datetime
from itertools import chain
import unicodedata
import pandas as pd
import requests
from multiprocessing import Pool

from sklearn.preprocessing import MinMaxScaler

import Player


# calculate stats based on given weights and row of stats
def calculateStat(row, weights):
    
    # Incorporate the relationship between OTPM and PPG
    ratio = 0.18  # from empirical testing
    composite_feature = ratio * row['OTPM'] + (1 - ratio) * row['PPG']

    # Replace OTPM and PPG with the composite feature in the row
    row_without_otpm_ppg = row.drop(['OTPM', 'PPG'])
    row_with_composite = row_without_otpm_ppg._append(pd.Series([composite_feature], index=['Composite_OTPM_PPG']))

    if len(weights) != len(row_with_composite):
        raise ValueError("Number of weights must match the number of features.")
    
    if round(sum(weights), 2) != 1:
        print(sum(weights))
        raise ValueError("Weights must add up to 1.")

    # Calculate the overallStat using the modified row
    overallStat = sum(w * stat for w, stat in zip(weights, row_with_composite))
    return overallStat

def calculateStatNoComp(row, weights):
    
    if len(weights) != len(row):
        raise ValueError("Number of weights must match the number of features.")
    
    if round(sum(weights), 2) != 1:
        print(sum(weights))
        raise ValueError("Weights must add up to 1.")

    # Calculate the overallStat using the modified row
    overallStat = sum(w * stat for w, stat in zip(weights, row))
    return overallStat


def test():
    # Load the data
    try:
        data = pd.read_csv('lib/data.csv')
    except UnicodeDecodeError:
        print("Manually save the csv file and try again.\n")
        exit(1)

    features = data[['GPG', 'Last 5 GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home (1)']]
    labels = data['Scored']
    names = data['Name']
    teams = data['Team']
    bets = data['Bet']
    ids = data['ID']

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(features)

    # The normalized_features is now a numpy array, you can convert it back to a DataFrame if needed
    normalized_features_df = pd.DataFrame(normalized_features, columns=features.columns)

    # Normalized weights
    weights = [0.2, 0.3, 0.1, 0.1, 0.2, 0.0, 0.1, 0.0]

    # weights = empiricalTest()
    players = []

    for index, normalized_row in normalized_features_df.iterrows():

        # Access label for the current row
        label = labels.loc[index]
        if label == ' ':

            # Your further logic with the normalized features and label
            probability = calculateStatNoComp(normalized_row, weights)
            players.append(Player.Player(names[index], -1, -1, -1, -1, -1, -1, -1))
            
            players[-1].setId(ids[index])

            players[-1].setStat(probability)
            players[-1].setGPG(features['GPG'][index])
            players[-1].setTeamName(teams[index])
            if bets[index] > 0:
                players[-1].setBet(f"+{bets[index]}")
            else:
                players[-1].setBet(bets[index])
            players[-1].set5GPG(features['Last 5 GPG'][index])
            players[-1].setHGPG(features['HGPG'][index])
            players[-1].setPPG(features['PPG'][index])
            players[-1].setOTPM(features['OTPM'][index])
            players[-1].setTGPG(features['TGPG'][index])
            players[-1].setOTGA(features['OTGA'][index])
            players[-1].setHome(features['Home (1)'][index])

    return players


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
    target_date = datetime.date.today().strftime('%Y-%m-%d')
    # target_date = "2024-02-19"

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
    # allPlayers = getAllPlayers()
    allPlayers = test()
    allPlayers = sorted(allPlayers, reverse=True)
    Player.Player.printHeader()

    i=1
    for player in allPlayers:
        print(f"{i}\t{player}")
        i+=1

    threshold = 0.48
    print("\n\nBet on:")
    for player in allPlayers:
        if player.getStat() >= threshold:
            print(player)

if __name__ == "__main__":
    rank()
    