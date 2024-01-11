import requests
import json
import pandas as pd
import time
import math
import pandas as pd
import tensorflow as tf


class Player:

    allRosters = []

    def __str__(self):
        return (f"{self.__name} : {self.__stat}")
    
    def getStat(self):
        return self.__stat
    
    def getName(self):
        return self.__name
    

    # helper functions
    # there has to be a better way to do this
    def __fixName(self, first_name, last_name):
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

        return first_name+" "+last_name


    def __getPlayerID(self, name):
        base_url = "https://statsapi.web.nhl.com/api/v1/teams/"
        # 1-10, 12-30, 52-54
        team_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 52, 53, 54]

        # this has to rather be changed yearly or set up using datetime
        for i in team_ids:
            try:
                # this has to rather be changed yearly or set up using datetime
                # url = base_url + str(i) + "/roster/" + "?season=" + "20232024"
                df_roster = self.allRosters[i]
                id = df_roster[df_roster['person.fullName'].str.contains(name)]['person.id'].values[0]
                self.__team = i
                return id
            except:
                pass
        
        return -1
    
    # 5 seasons was 103 correct (55 33 17)
    # 4 seasons was 110 correct (55 35 20)
    # 3 seasons was 110 correct (55 35 20)
    # 2 seasons was 118 correct (58 36 24)
    # 1 season was 111 correct (64 33 14)
    def __getGPGP(self, playerID, seasons=2):
        # how many seasons to look back on

        final_GPGP=0
        # url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats/?stats=yearByYear'
        url = "https://statsapi.web.nhl.com/api/v1/people/8479318/stats/?stats=yearByYear"
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
    

    def __getTeam(self, playerID):
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


    def __getGPGFT(self, playerID):
        teamID = self.__team
        if teamID == -1:
            return -1
        URL = "https://statsapi.web.nhl.com/api/v1/teams/" + str(teamID) + "/stats"
        response = requests.get(URL)
        tgpg = json.loads(response.content)
        try:
            tgpg = tgpg['stats'][0]['splits'][0]['stat']['goalsPerGame']
        except:
            # if tgpg cannot be found, give average of 3
            # this should never happen since i changed how we get playerID
            print(playerID)
            tgpg = 3 

        return tgpg
    

    def printTime(self, allSeconds):
        seconds = allSeconds
        minutes = math.floor(seconds / 60)
        seconds = seconds - (minutes * 60)

        hours = math.floor(minutes / 60)
        minutes = minutes - (hours * 60)

        seconds = math.floor(seconds)


        # print float??
        print("--- %lf seconds ---" %seconds)
    

    def __calculateStat(self):
        # return (self.__goalsPerGame * self.__tgpg)
        return (self.__goalsPerGame)
    
    @classmethod
    def initTeamsRosters(cls):
        base_url = "https://statsapi.web.nhl.com/api/v1/teams/"
        team_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 52, 53, 54]
        for i in team_ids:
            # this has to rather be changed yearly or set up using datetime
            print(f"Loading roster data for team {i}")
            url = base_url + str(i) + "/roster/" + "?season=" + "20232024"
            df_roster = pd.json_normalize(requests.get(url).json()["roster"]).astype(str)
            cls.allRosters.append(df_roster)

        return
        # return allRosters[allRosters.index(teamID)]    

    def __init__(self, name, id=-1): # type: ignore
        if (name == ""):
            return
        # change to first and last name
        self.__name = self.__fixName(name.split()[0], name.split()[1])

        # get playerID
        #startTime = time.time()
        if (id == -1):
            self.__playerID = self.__getPlayerID(self.__name)
        else:
            self.__playerID = id

        #endTime = time.time()
        #timeElapsed = endTime - startTime
        #self.printTime(timeElapsed)
        if self.__playerID == -1:
            # player's team (and id) could not be found
            self.__goalsPerGame = 0
            self.__tgpg = 0
            self.__stat = 0
        else:
            # calculates a player's goals per game
            self.__goalsPerGame = self.__getGPGP(self.__playerID)

            # team gpg
            # self.__tgpg = self.__getGPGFT(self.__playerID)

            # stat
            self.__stat = self.__calculateStat()

    def __init__(self, firstName, lastName, id=-1):

        # change to first and last name
        self.__name = self.__fixName(firstName, lastName)

        # get playerID
        #startTime = time.time()
        if (id == -1):
            self.__playerID = self.__getPlayerID(self.__name)
        #endTime = time.time()
        #timeElapsed = endTime - startTime
        #self.printTime(timeElapsed)
        if self.__playerID == -1:
            # player's team (and id) could not be found
            self.__goalsPerGame = 0
            self.__tgpg = 0
            self.__stat = 0
        else:
            # calculates a player's goals per game
            self.__goalsPerGame = self.__getGPGP(self.__playerID)

            # team gpg
            # self.__tgpg = self.__getGPGFT(self.__playerID)

            # stat
            self.__stat = self.__calculateStat()


