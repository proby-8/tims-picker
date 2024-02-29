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

def find_PPG(player_name, data):
    for player in data["skaters"]:
        full_name = f"{player['firstName']['default']} {player['lastName']['default']}"
        if full_name.lower() == player_name.lower():
            return player['powerPlayGoals']
    return 0.0

class Player:

    teamStats = {}
    
    def getStat(self):
        return self.__stat
    
    def setStat(self, stat):
        self.__stat = stat

    def setBet(self, bet):
        self.__bet = bet

    def getBet(self):
        return self.__bet
    
    def setName(self, name):
        self.__name = name
    
    def getName(self):
        return self.__name
    
    def setId(self, id):
        self.__id = id
    
    def getId(self):
        return self.__playerID
    
    def setGPG(self, gpg):
        self.__goalsPerGame = gpg
    
    def getGPG(self):
        return self.__goalsPerGame
    
    def set5GPG(self, gpg5):
        self.__5GPG = gpg5

    def setPPG(self, ppg):
        self.__PPG = ppg

    def setOTPM(self, otpm):
        self.__OTPM = otpm
    
    def setHGPG(self, hgpg):
        self.__historicGPG = hgpg
    
    def getHGPG(self):
        return self.__historicGPG
    
    def setTGPG(self, tgpg):
        self.__teamGoalsPerGame = tgpg
    
    def getTGPG(self):
        return self.__teamGoalsPerGame
    
    def setHome(self, isHome):
        self.__isHome = isHome
    
    def setOTGA(self, otga):
        self.__otherTeamGoalsAgainst = otga
    
    def getOTGA(self):
        return self.__otherTeamGoalsAgainst
    
    def setTeamName(self, teamName):
        self.__teamName = teamName
    
    def getTeamName(self):
        return self.__teamName
    
    def getTeamAbbr(self):
        return self.__teamAbbr
    
    def getTeamId(self):
        return self.__teamId
    
    @classmethod
    def initTeamStats( cls, teamId, otherTeamId ):
        url = f"https://api.nhle.com/stats/rest/en/team/summary?cayenneExp=seasonId=20232024%20and%20gameTypeId=2"
        r = requests.get(url)
        data = r.json()

        url2 = f"https://api.nhle.com/stats/rest/en/team/penaltykilltime?cayenneExp=seasonId=20232024%20and%20gameTypeId=2"
        r2 = requests.get(url2)
        data2 = r2.json()

        for team in data["data"]:
            if (teamId == team['teamId'] or otherTeamId == team['teamId']):
                cls.teamStats[team['teamId']] = {
                                            "gpg" : team["goalsForPerGame"],
                                            "ga"  : team['goalsAgainstPerGame']
                                        }

        for team in data2["data"]:
            if (teamId == team['teamId'] or otherTeamId == team['teamId']):
                cls.teamStats[team['teamId']].update({
                                            "pm" : team["timeOnIceShorthanded"]
                                        })


    @classmethod
    def printHeader ( cls ):
        print("\nPlayers in order:")

        name_padding = 30
        team_padding = 15
        stat_padding = 10

        print("\t{:<{}} {:<{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}}".format(
            "Player Name", name_padding,
            "Team Name", team_padding,
            "Bet", stat_padding,
            "Stat", stat_padding,
            "GPG", stat_padding,
            "5GPG", stat_padding,
            "HGPG", stat_padding,
            "HPPG", stat_padding,
            "OTPM", stat_padding,
            "TGPG", stat_padding,
            "OTGA", stat_padding,
            "isHome", stat_padding
        ))
        print("") 
    
    def getFeatures(self):
        return {
            'GPG' : self.__goalsPerGame,
            "TGPG": self.__teamGoalsPerGame,
            "OTGA" : self.__otherTeamGoalsAgainst,
            # "Last 5 GPG" : self.__5GPG,
            # "HGPG": self.__historicGPG,
            # "PPG": self.__PPG,
            # "OTPM": self.__OTPM,
            # "Home (1)" : self.__isHome,
            # 'Bet': self.__bet,
        }
    
    def findHistoricGPG(self):

        ppg = 0
        goals = 0
        games = 0
        acceptableSeasons = [20232024, 20222023, 20212022]
        for season_data in self.__playerData['seasonTotals']:
            if ((season_data['season'] in acceptableSeasons) and (season_data['leagueAbbrev'] == "NHL")):
                try:
                    tempPPG = season_data['powerPlayGoals']
                    tempGoals = season_data['goals']
                    tempGames = season_data['gamesPlayed']

                    ppg += tempPPG
                    goals += tempGoals
                    games += tempGames
                except:
                    # weird
                    pass

        self.__PPG = ppg

        if games == 0:
            return 0
        
        return goals/games


    def findLast5GPG(self):
        goals = 0
        games = 5
        try:
            for game_data in self.__playerData['last5Games']:
                goals += game_data['goals']
        except KeyError:
            return 0
            
        return goals/games
            

    def __init__(self, name, id, teamName, teamAbbr, teamId, otherTeamId, isHome, data):
        if (name == ""):
            return
        self.__name = name
        
        if (data != -1):
            url = f"https://api-web.nhle.com/v1/player/{id}/landing"
            r = requests.get(url)
            self.__playerData = r.json()

            self.__playerID = id
            self.__teamId = teamId
            self.__teamName = teamName
            self.__otherTeamId = otherTeamId
            self.__bet = '0'

            self.__isHome = isHome
            self.__goalsPerGame = find_GPGP(self.getName(), data)
            self.__historicGPG = self.findHistoricGPG()
            # self.__PPG = find_PPG(self.getName(), data)
            self.__5GPG = self.findLast5GPG()
            
            # teams goals per game
            self.__teamGoalsPerGame = Player.teamStats[self.__teamId]['gpg']
            
            # other team goals against
            self.__otherTeamGoalsAgainst = Player.teamStats[self.__otherTeamId]['ga']

            self.__OTPM = Player.teamStats[self.__otherTeamId]['pm']
            
            # stat
            self.__stat = 0

    # calculate stats based on given weights and row of stats
    def calculateStat( self ):

        weights = [
            0.0,
            0.4,
            0.3,
            0.0,
            0.0,
            0.1,
            0.2
        ]
        
        # Incorporate the relationship between OTPM and PPG
        ratio = 0.18  # from empirical testing
        
        row = self.getFeatures()
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
    
    def toCSV(self):
        csv_format = "{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
            ' ',
            self.getName(),
            self.getId(),
            self.getTeamName(),
            "{:s}".format(self.__bet),
            "{:f}".format(self.__goalsPerGame),
            "{:f}".format(self.__5GPG),
            "{:f}".format(self.__historicGPG),
            "{:f}".format(self.__PPG),
            "{:d}".format(self.__OTPM),
            "{:f}".format(self.__teamGoalsPerGame),
            "{:f}".format(self.__otherTeamGoalsAgainst),
            "{:d}".format(self.__isHome)
        )
        return csv_format+"\n"
    
    @classmethod
    def headerToCSV(self):
        csv_format = "{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
            "Data",
            "Scored",
            "Name",
            "ID",
            "Team",
            "Bet",
            "GPG",
            "Last 5 GPG",
            "HGPG",
            "PPG",
            "OTPM",
            "TGPG",
            "OTGA",
            "Home (1)"
        )
        return csv_format+"\n"


    # to string method
    def __str__ (self):
        name_padding = 30
        team_padding = 15
        stat_padding = 10

        return "{:<{}} {:<{}} {:<{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}} {:>{}}".format(
            self.getName(), name_padding, 
            self.getTeamName(), team_padding, 
            "{:s}".format(str(self.__bet)), stat_padding, 
            "{:.10f}".format(float(self.__stat)), stat_padding, 
            "{:.2f}".format(self.__goalsPerGame), stat_padding, 
            "{:.2f}".format(self.__5GPG), stat_padding, 
            "{:.2f}".format(self.__historicGPG), stat_padding, 
            "{:.2f}".format(self.__PPG), stat_padding, 
            "{:d}".format(self.__OTPM), stat_padding,## Function 2: Make a Guess Using an AI Formulated Calculation

            "{:.2f}".format(self.__teamGoalsPerGame), stat_padding, 
            "{:.2f}".format(self.__otherTeamGoalsAgainst), stat_padding, 
            "{:d}".format(self.__isHome), stat_padding
        )
    
    def toJSON(self):
        return {
            'name': str(self.getName()),
            'team_name': str(self.__teamName),  # Assuming __teamName is a string
            'bet': float(self.__bet),           # Casting to float
            'stat': float(self.__stat),           # Casting to int
            'goals_per_game': float(self.__goalsPerGame),
            'five_gpg': float(self.__5GPG),
            'historic_gpg': float(self.__historicGPG),
            'ppg': float(self.__PPG),
            'otpm': float(self.__OTPM),
            'team_goals_per_game': float(self.__teamGoalsPerGame),
            'other_team_goals_against': float(self.__otherTeamGoalsAgainst),
            'is_home': int(self.__isHome)      # Assuming __isHome is boolean
        }

