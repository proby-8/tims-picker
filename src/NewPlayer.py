import requests
import json
import pandas as pd
import pandas as pd


class Player:
    
    def getStat(self):
        return self.__stat
    
    def getName(self):
        return self.__name
    
    def __init__(self, name, id):
        if (name == ""):
            return
        # change to first and last name
        self.__name = name

        # get playerID
        #startTime = time.time()
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
    
    # 5 seasons was 103 correct (55 33 17)
    # 4 seasons was 110 correct (55 35 20)
    # 3 seasons was 110 correct (55 35 20)
    # 2 seasons was 118 correct (58 36 24)
    # 1 season was 111 correct (64 33 14)
    def __getGPGP(self, playerID, seasons=2):
        # how many seasons to look back on

        final_GPGP=0
        url = 'https://api-web.nhle.com/v1/player/' + str(playerID) + '/landing'

        try:
            response = requests.get(url)
            content = json.loads(response.content)
        except:
            return -1
        
        current_season_stats = content['featuredStats']['regularSeason']['subSeason']

        # Extract goals and games played
        goals = current_season_stats['goals']
        games_played = current_season_stats['gamesPlayed']

        final_GPGP = goals / games_played

        return final_GPGP

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

    def __calculateStat(self):
        # return (self.__goalsPerGame * self.__tgpg)
        return (self.__goalsPerGame)

    def __lt__(self, other):
        return self.__stat < other.__stat

    def __le__(self, other):
        return self.__stat <= other.__stat

    def __eq__(self, other):
        return self.__stat == other.__stat

    def __ne__(self, other):
        return self.__stat != other.__stat

    def __gt__(self, other):
        return self.__stat > other.__stat

    def __ge__(self, other):
        return self.__stat >= other.__stat

    def __str__ (self):
        name_padding = 30
        stat_padding = 10
        return "{:<{}} {:>{}}".format(self.getName(), name_padding, "{:.2f}".format(self.getStat()), stat_padding)