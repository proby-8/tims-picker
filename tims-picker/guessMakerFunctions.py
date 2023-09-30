import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import math


def getPlayerNames(date, round, group): 
    URL = "http://www.hockeychallengepicks.ca/history/" + date + str(round)
    try:
        page = requests.get(URL)
    except:
        print("Fatal error: Could not connect to source of player names.")
        exit(1)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="pick-" + str(group))

    players_fullName = []
    x=0
    player = results.find_all("tr")
    for p in player:
        p = p.find("a")
        p = (str) (p)
        p = p[114:-4]

        players_fullName.append(p)
        x = x + 1

    return players_fullName


def fixName (first_name, last_name, name):
    if (first_name == "Mitch") & (last_name == "Marner"):
        first_name = "Mitchell"
    if (first_name == "Zachary") & (last_name == "Aston-Reese"):
        first_name = "Zach"
    if (first_name == "Jani") & (last_name == "Hakanpaa"):
        last_name = "Hakanpää"
    if (first_name == "Alexander") & (last_name == "Wennberg"):
        last_name = "Alex"
    if (first_name == "T.J.") & (last_name == "Brodie"):
        first_name = "TJ"
    if (first_name == "Tim") & (last_name == "Stutzle"):
        last_name = "Stützle"
    if (first_name == "Alexis") & (last_name == "Lafreniere"):
        last_name = "Lafrenière"
    if (first_name == "Christopher") & (last_name == "Tanev"):
        first_name = "Chris"

    if name == "first":
        return first_name
    else:
        return last_name


def getPlayerID(first_name, last_name):
    base_url = 'https://suggest.svc.nhl.com/svc/suggest/v1/minplayers/'

    full_url = base_url + first_name + '%20' + last_name + '/1'
    response = requests.get(full_url)
    try:
        suggestions = json.loads(response.content)['suggestions'][0]
    except:
        # some names are different in tims vs nhl api
        first_name = fixName(first_name, last_name, "first")
        last_name = fixName(first_name, last_name, "last")
        full_url = base_url + first_name + '%20' + last_name + '/1'
        response = requests.get(full_url)
        suggestions = json.loads(response.content)['suggestions'][0]
    player_info = str.split(suggestions, "|")

    return player_info[0]


def getGPGP(playerID, seasons=3):
    # how many seasons to look back on

    final_GPGP=0
    url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats/?stats=yearByYear'
    response = requests.get(url)
    content = json.loads(response.content)['stats']
    splits = content[0]['splits']
    df_splits = (pd.json_normalize(splits, sep = "_" ).query('league_name == "National Hockey League"'))
    gpg = df_splits['stat_goals']/df_splits['stat_games']

    count=0
    loop=0
    for gpgps in gpg:
        count+=1
    for gpgps in gpg:
        if loop >= (count-seasons):
            final_GPGP += gpgps
        loop+=1
    final_GPGP /= seasons

    return final_GPGP


def getTeam(playerID):
    url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/'
    try:
        response = requests.get(url)
        theirTeamID = json.loads(response.content)['people'][0]['currentTeam']['id']
        # teamName = json.loads(response.content)['people'][0]['currentTeam']['name']
    except:
        # if the API doesn't have the team this guy is on
        theirTeamID = -1
        # teamName = ""
    
    return theirTeamID


def getTeamAgainst(date, teamName):

    URL = "https://statsapi.web.nhl.com/api/v1/schedule?date=" + str(date)
    response = requests.get(URL)
    content = json.loads(response.content)['dates']
    numGames = content[0]['totalGames']
    games = content[0]['games']

    x=0
    gameList = []
    while x < numGames:
        gameList.append(games[x]['gamePk'])
        awayTeam = games[x]['teams']['away']['team']['name']
        homeTeam = games[x]['teams']['home']['team']['name']

        if (homeTeam == teamName):
            return awayTeam
        if (awayTeam == teamName):
            return homeTeam
        x+=1

    return -1


def getGPGAT(playerID, date):

    url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/'
    try:
        response = requests.get(url)
        # theirTeamID = json.loads(response.content)['people'][0]['currentTeam']['id']
        teamName = json.loads(response.content)['people'][0]['currentTeam']['name']
    except:
        # if the API doesn't have the team this guy is on for some reason
        # theirTeamID = -1
        teamName = ""

    teamAgainst = getTeamAgainst(date, teamName)
    if teamAgainst == -1:
        return -1
    url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=vsTeam&season=20212022'
    response = requests.get(url)
    content = json.loads(response.content)['stats']
    splits = content[0]['splits']

    x = 0
    try:
        while (x<32):
            if (splits[x]['opponent']['name'] == teamAgainst):
                stat = splits[x]['stat']
                goalsPerGame = stat['goals'] / stat['games']
                x=500
            x+=1
    except:
        return -1
    
    return goalsPerGame


def getGPGFT(playerID):
    teamID = getTeam(playerID)
    URL = "https://statsapi.web.nhl.com/api/v1/teams/" + str(teamID) + "/stats"
    response = requests.get(URL)
    tgpg = json.loads(response.content)
    try:
        tgpg = tgpg['stats'][0]['splits'][0]['stat']['goalsPerGame']
    except:
        # if tgpg cannot be found, give average of 3
        tgpg = 3 
    return tgpg


def printTime(allSeconds):
    seconds = allSeconds
    minutes = math.floor(seconds / 60)
    seconds = seconds - (minutes * 60)

    hours = math.floor(minutes / 60)
    minutes = minutes - (hours * 60)

    seconds = math.floor(seconds)

    print("--- %d hours ---" %hours)
    print("--- %d minutes ---" %minutes)
    print("--- %d seconds ---" %seconds)