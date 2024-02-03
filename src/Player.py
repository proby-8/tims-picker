import requests
import json
import pandas as pd

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
    
    def getGPG(self):
        return self.__goalsPerGame
    
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
    def initTeamStats( cls ):
        url = f"https://api.nhle.com/stats/rest/en/team/summary?cayenneExp=seasonId=20232024%20and%20gameTypeId=2"
        r = requests.get(url)
        data = r.json()

        for team in data["data"]:
            teamId = team["teamId"]
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

    def __init__(self, name, id, teamName, teamAbbr, teamId, otherTeamId, data):
        if (name == ""):
            return

        self.__name = name
        self.__playerID = id
        self.__teamId = teamId
        self.__otherTeamId = otherTeamId

        if self.__playerID == -1:
            # player's team (and id) could not be found
            self.__stat = -1
        else:
            # calculates a player's goals per game
            if (data):
                self.__goalsPerGame = find_GPGP(self.getName(), data)
            else:
                self.__goalsPerGame = self.__getGPGP(self.__playerID)

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
        return "{:<{}} {:>{}} {:>{}} {:>{}} {:>{}}".format(self.getName(), name_padding, "{:.2f}".format(float(self.__stat)), stat_padding, "{:.2f}".format(self.__goalsPerGame), stat_padding, "{:.2f}".format(self.__teamGoalsPerGame), stat_padding, "{:.2f}".format(self.__otherTeamGoalsAgainst), stat_padding)
