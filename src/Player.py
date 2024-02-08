import sys
import time
import requests
import json
import pandas as pd
import sys


def find_GPGP(player_name, data):
    for player in data["skaters"]:
        full_name = f"{player['firstName']['default']} {player['lastName']['default']}"
        if full_name.lower() == player_name.lower():
            return player['goals'] / player['gamesPlayed']
    return 0.0

class Player:

    teamStats = {}
    
    def getStat(self):
        return self.__stat
    
    def getName(self):
        return self.__name
    
    def getId(self):
        return self.__playerID
    
    def getGPG(self):
        return self.__goalsPerGame
    
    def getHGPG(self):
        return self.__historicGPG
    
    def getTGPG(self):
        return self.__teamGoalsPerGame
    
    def getOTGA(self):
        return self.__otherTeamGoalsAgainst
    
    def getTeamName(self):
        return self.__teamName
    
    def getTeamAbbr(self):
        return self.__teamAbbr
    
    def getTeamId(self):
        return self.__teamId
    
    @classmethod
    def initTeamStats( cls, teamId ):
        url = f"https://api.nhle.com/stats/rest/en/team/summary?cayenneExp=seasonId=20232024%20and%20gameTypeId=2"
        r = requests.get(url)
        data = r.json()

        for team in data["data"]:
            if (teamId == team['teamId'] or (teamId == -1)):
                cls.teamStats[teamId] = {
                                            "gpg" : team["goalsForPerGame"],
                                            "ga"  : team['goalsAgainstPerGame']
                                        }
    
    def getFeatures(self):
        return {
            'Goals per Game' : self.__goalsPerGame,
            "Team's Goals per Game" : self.__teamGoalsPerGame,
            "Other Team's Goals Against" : self.__otherTeamGoalsAgainst
        }
    
    def findHistoricGPG(self):

        goals = 0
        games = 0
        acceptableSeasons = [20232024, 20222023, 20212022]
        for season_data in self.__playerData['seasonTotals']:
            if ((season_data['season'] in acceptableSeasons) and (season_data['leagueAbbrev'] == "NHL")):
                try:

                    tempGoals = season_data['goals']
                    tempGames = season_data['gamesPlayed']

                    goals += tempGoals
                    games += tempGames
                except:
                    # weird
                    pass

        if games == 0:
            return 0
        
        return goals/games


    def findLast5GPG(self):

        goals = 0
        games = 5
        for game_data in self.__playerData['last5Games']:
            goals += game_data['goals']
      
        return goals/games

    def __init__(self, name, id, teamName, teamAbbr, teamId, otherTeamId, data):
        if (name == ""):
            return

        self.__name = name
        self.__playerID = id
        self.__teamId = teamId
        self.__otherTeamId = otherTeamId

        url = f"https://api-web.nhle.com/v1/player/{id}/landing"
        r = requests.get(url)
        self.__playerData = r.json()

        # calculates a player's goals per game
        self.__goalsPerGame = find_GPGP(self.getName(), data)
        self.__historicGPG = self.findHistoricGPG()
        self.__5GPG = self.findLast5GPG()
        
        # teams goals per game
        self.__teamGoalsPerGame = Player.teamStats[self.__teamId]['gpg']
        
        # other team goals against
        self.__otherTeamGoalsAgainst = Player.teamStats[self.__teamId]['ga']

        # stat
        self.__stat = self.__calculateStat()

    def __calculateStat(self):
        # return (self.__goalsPerGame * self.__tgpg)
        return (self.__goalsPerGame * self.__teamGoalsPerGame * self.__otherTeamGoalsAgainst)

    # For comparison
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

    # to string method
    def __str__ (self):
        name_padding = 30
        stat_padding = 10
        return "{:<{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}}".format(self.getName(), name_padding, "{:.2f}".format(float(self.__stat)), stat_padding, "{:.2f}".format(self.__goalsPerGame), stat_padding, "{:.2f}".format(self.__5GPG), stat_padding, "{:.2f}".format(self.__historicGPG), stat_padding, "{:.2f}".format(self.__teamGoalsPerGame), stat_padding, "{:.2f}".format(self.__otherTeamGoalsAgainst), stat_padding)
