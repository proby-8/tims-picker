import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import datetime
import time
import math

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

def addDays(startdate, daysChange=1):
    enddate = pd.to_datetime(startdate) + pd.DateOffset(days=daysChange)
    enddate = str(enddate)
    return enddate[:-9]

def subtractDays(startDate, daysChange=1):
    enddate = pd.to_datetime(startDate) + pd.DateOffset(days=-daysChange)
    enddate = str(enddate)
    return enddate[:-9]


def getStats(path, date, daysToLookAt, daysGoingUp):
    daysSkipped = 0
    startTime = time.time()
    for i in range(0,int(daysToLookAt)):
        print("Currently on day " + str(date))
        skipDay = False
        try:
            players_fullName = (getPlayerNames(date, 1))
        except:
            # no data available for this
            skipDay = True 
            daysSkipped +=1
        
        if (skipDay == False):
            goalScorers = getGoalScorers(date)
            for group in range(1,4):
                players_fullName = (getPlayerNames(date, group))
                df = pd.DataFrame (players_fullName)

                # list items for each group
                dates = []
                players_firstName = []
                players_lastName = []
                gpg = []
                tgpg = []
                otga = []
                playerScored = []

                for i in range(0,len(players_fullName)):
                    # get the date
                    dates.append(date)

                    # this part getes players first and last name
                    both = players_fullName[i].split()
                    players_firstName.append(both[0])
                    players_lastName.append(both[1])

                    # this gets a player's id number
                    playerID = getPlayerID(players_firstName[i], players_lastName[i])

                    # get all the stats

                    if players_fullName[i] in goalScorers:
                        playerScored.append(1)
                    else:
                        playerScored.append(0)

                    # calculates a players goals per game (if player scored day of, average doesnt adjust for this)
                    gpg.append(getGPGP(playerID, playerScored))

                    # team gpg
                    tgpg.append(getGPGFT(playerID))

                    # other teams goals against
                    otga.append(getOtherTeamGA(playerID, date))

                # create dataframe
                dfnames = pd.DataFrame(players_fullName)
                dfgpg = pd.DataFrame (gpg)
                dfplayerScored = pd.DataFrame (playerScored)
                dfdates = pd.DataFrame (dates)
                dftgpg = pd.DataFrame (tgpg)
                dfotga = pd.DataFrame (otga)
                df = pd.concat([dfdates, dfplayerScored, dfnames, dfgpg, dftgpg, dfotga], axis=1, sort=False)

                # write to file here
                if daysGoingUp:
                    oldDF = pd.read_csv(path + "train_test" + str(group) + ".csv")
                    df = df.set_axis(['Date', 'Scored', 'Name', 'Goals per Game', "Team's Goals per Game", "Other Team's Goals Against"], axis=1)
                    df.to_csv(path + "train_test" + str(group) + ".csv", index=False, header=True, mode='w')
                    oldDF.to_csv(path + "train_test" + str(group) + ".csv", index=False, header=False, mode='a')
                else:                   
                    todayDate = datetime.datetime.today().strftime('%Y-%m-%d')
                    todayDate = subtractDays(todayDate)
                    keepHeader=False
                    if (date == todayDate):
                        df = df.set_axis(['Date', 'Scored', 'Name', 'Goals per Game', "Team's Goals per Game", "Other Team's Goals Against"], axis=1)
                        keepHeader = True
                    df.to_csv(path + "train_test" + str(group) + ".csv", index=False, header=keepHeader, mode='a')
            
        if daysGoingUp:
            date = addDays(date, 1)
        else:
            date = subtractDays(date, 1)

    if ((int(daysSkipped)) == (int(daysToLookAt))):
        print("Every day was skipped")
        # loop to find the next possible day
        keepGoing = True
        while (keepGoing):
            print(date)
            try:
                players_fullName = (getPlayerNames(date, 1))
                keepGoing = False
            except:
                date = subtractDays(date)
        print(f"Next possible date: {date}")

    else:
        print("Average time per day (not including skipped days): ", end="")
        totalSeconds = time.time() - startTime
        print(round(totalSeconds/((int(daysToLookAt))-(int(daysSkipped))),3))
        print(f"{daysSkipped} days were skipped")


def getPlayerNames(date, group): 
    # URL = "http://www.hockeychallengepicks.ca/history/2023-02-01/1"
    URL = (F"http://www.hockeychallengepicks.ca/history/{date}/1")
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="pick-" + str(group))

    players_fullName = []

    player = results.find_all("tr")
    # print(player)
    for p in player:
        # print("NEW LOOP\n\n\n")
        p = p.find("a")
        p = (str) (p)
        p = p[114:-4]
        # print(p)

        players_fullName.append(p)

    return players_fullName


def getPlayerID(first_name, last_name):
    base_url = 'https://suggest.svc.nhl.com/svc/suggest/v1/minplayers/'

    num_to_return = '1'
 
    full_url = base_url + first_name + '%20' + last_name + '/' + num_to_return
    response = requests.get(full_url)
    try:
        suggestions = json.loads(response.content)['suggestions'][0]
    except:
        first_name = fixName(first_name, last_name, "first")
        last_name = fixName(first_name, last_name, "last")
        full_url = base_url + first_name + '%20' + last_name + '/' + num_to_return
        response = requests.get(full_url)
        try:
          suggestions = json.loads(response.content)['suggestions'][0]
        except:
            print("The following name failed: ")
            print(first_name+ " " +last_name)

    # print(suggestions)
    player_info = str.split(suggestions, "|")

    return player_info[0]


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
    # webscrape name from nhl website


def getGPGP(playerID, playerScored, seasons=3):
    # how many seasons to look back on

    final_GPGP=0
    url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats/?stats=yearByYear'
    response = requests.get(url)
    content = json.loads(response.content)['stats']
    splits = content[0]['splits']
    df_splits = (pd.json_normalize(splits, sep = "_" ).query('league_name == "National Hockey League"'))
    if playerScored:
        gpg = (df_splits['stat_goals']) / (df_splits['stat_games'])
    else:
        gpg = (df_splits['stat_goals']) / (df_splits['stat_games'])

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


def getOtherTeamGA(playerID, date):
    url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/'
    # print(url)
    try:
        response = requests.get(url)
        theirTeamID = json.loads(response.content)['people'][0]['currentTeam']['id']
        teamName = json.loads(response.content)['people'][0]['currentTeam']['name']
        # print(content)
    except:
        # if the API doesn't have the team this guy is on
        theirTeamID = -1
        teamName = ""

    teamID = getTeamAgainstID(date, theirTeamID, teamName)
    if teamID == -1:
        return -1
    
    # print(teamAgainst)

    # now we get GA average
    URL = "https://statsapi.web.nhl.com/api/v1/teams/" + str(teamID) + "/stats"

    response = requests.get(URL)
    # print(URL)

    tgpg = json.loads(response.content)
    try:
        tgpg = tgpg['stats'][0]['splits'][0]['stat']['goalsAgainstPerGame']
    except:
        tgpg = 3 # hopefully thats around average

    return tgpg


def getTeamAgainstID(date, theirTeamID, teamName):
    URL = "https://statsapi.web.nhl.com/api/v1/schedule?date=" + str(date)
    # print(URL)

    response = requests.get(URL)
    # print(URL)

    content = json.loads(response.content)['dates']
    numGames = content[0]['totalGames']
    #print(numGames)

    games = content[0]['games']
    # print(games)

    x=0
    gameList = []
    while x < numGames:
        gameList.append(games[x]['gamePk'])
        awayTeam = games[x]['teams']['away']['team']['name']
        homeTeam = games[x]['teams']['home']['team']['name']
        awayTeamID = games[x]['teams']['away']['team']['id']
        homeTeamID = games[x]['teams']['home']['team']['id']
        # print(awayTeam)
        # print(homeTeam)

        if (homeTeam == teamName):
            return awayTeamID
        if (awayTeam == teamName):
            return homeTeamID
        x+=1
    # print(gameList)

    return 1


def getGoalScorers(date):

    goalScorers = []

    URL = "https://statsapi.web.nhl.com/api/v1/schedule?date=" + str(date)

    response = requests.get(URL)
    # print(URL)
    
    try:
        content = json.loads(response.content)['dates']
        numGames = content[0]['totalGames']
        #print(numGames)
    except:
        return -1

    games = content[0]['games']
    # print(games)

    x=0
    gameList = []
    while x < numGames:
        gameList.append(games[x]['gamePk'])
        awayTeams = games[x]['teams']['away']['team']['name']
        homeTeams = games[x]['teams']['home']['team']['name']
        #print(awayTeams)
        #print(homeTeams)
        x+=1
    # print(gameList)

    x=0
    while x < numGames:
        URL = "https://statsapi.web.nhl.com/api/v1/game/" + str(gameList[x]) + "/feed/live"
        response = requests.get(URL)
        content = json.loads(response.content)['liveData']
        plays = content['plays']
        scoringPlays = plays['scoringPlays']

        plays = content['plays']['allPlays']
        for i in range(len(scoringPlays)):
            scoringPlay = plays[scoringPlays[i]]
            # print(scoringPlay)
            player = scoringPlay['players']
            for player in player:
                # print(player)
                if player['playerType'] == 'Scorer':
                    player = player['player']['fullName']
                    goalScorers.append(player)
                    # print(player)

        x+=1

    return goalScorers

