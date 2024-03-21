import requests
import pandas as pd

class Player:

    teamStats = {}

    # intializer for weightedGuess
    def __init__(self, name, teamName, id, gpg, gpg5, hgpg, ppg, otpm, tgpg, otga, isHome, bet=0, stat=0):
        if (name == ""):
            return
        
        self.__name = name
        self.__playerID = id
        self.__teamName = teamName
        self.__goalsPerGame = gpg
        self.__5GPG = gpg5
        self.__historicGPG = hgpg
        self.__PPG = ppg
        self.__OTPM = otpm
        self.__teamGoalsPerGame = tgpg
        self.__otherTeamGoalsAgainst = otga
        self.__isHome = isHome
        self.__bet = bet
        self.__stat = stat

    # accessor/mutator methods
    def setStat(self, stat):
        self.__stat = stat
        
    def getStat(self):
        return self.__stat

    def setBet(self, bet):
        self.__bet = bet

    def getBet(self):
        return self.__bet
    
    def setName(self, name):
        self.__name = name
    
    def getName(self):
        return self.__name
    
    def setId(self, id):
        self.__playerID = id
    
    def getId(self):
        return self.__playerID
    
    def setGPG(self, gpg):
        self.__goalsPerGame = gpg
    
    def getGPG(self):
        return self.__goalsPerGame
    
    def set5GPG(self, gpg5):
        self.__5GPG = gpg5
    
    def get5GPG(self):
        return self.__5GPG

    def setPPG(self, ppg):
        self.__PPG = ppg

    def getPPG(self):
        return self.__PPG

    def setOTPM(self, otpm):
        self.__OTPM = otpm

    def getOTPM(self):
        return self.__OTPM
    
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

    def isHome(self):
        return self.__isHome
    
    def setOTGA(self, otga):
        self.__otherTeamGoalsAgainst = otga
    
    def getOTGA(self):
        return self.__otherTeamGoalsAgainst
    
    def setTeamName(self, teamName):
        self.__teamName = teamName
    
    def getTeamName(self):
        return self.__teamName

    def setTeamAbbr(self, teamABBR):
        self.__teamAbbr = teamABBR 
       
    def getTeamAbbr(self):
        return self.__teamAbbr
    
    def setTeamId(self, teamID):
        self.__teamId = teamID
    
    def getTeamId(self):
        return self.__teamId
    
    # init all teams stats at once? More overhead for days with fewer games, but less api calls for each game

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
    
