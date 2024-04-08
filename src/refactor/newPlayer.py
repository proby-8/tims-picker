import requests
import pandas as pd

class Player:

    teamStats = {}

    @classmethod
    def noStatInit(cls, name, id, teamName, teamAbbr, teamId, otherTeamId, isHome, data):
        if (name == ""):
            return
        playerInstance = cls(name, teamName, id, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, isHome, 0, 0)
        
        url = f"https://api-web.nhle.com/v1/player/{id}/landing"
        r = requests.get(url)
        playerInstance.__playerData = r.json()

        playerInstance.__teamId = teamId
        playerInstance.__otherTeamId = otherTeamId
        playerInstance.__teamData = data
        
        playerInstance.__goalsPerGame = playerInstance.findGPGP()
        playerInstance.__5GPG = playerInstance.findLast5GPG()
        playerInstance.__historicGPG = playerInstance.findHistoricGPG()
        playerInstance.__PPG = playerInstance.find_PPG()
        playerInstance.__otherTeamGoalsAgainst = Player.teamStats[playerInstance.__otherTeamId]['ga']
        playerInstance.__teamGoalsPerGame = Player.teamStats[playerInstance.__teamId]['gpg']        
        playerInstance.__OTPM = Player.teamStats[playerInstance.__otherTeamId]['pm']
        playerInstance.__stat = 0

        return playerInstance

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
    
    # get stats
    def findGPGP(self):
        playerName = self.getName()
        for player in self.__teamData["skaters"]:
            full_name = f"{player['firstName']['default']} {player['lastName']['default']}"
            if full_name.lower() == playerName.lower():
                return player['goals'] / player['gamesPlayed']
        return 0.0

    def findLast5GPG(self):
        goals = 0
        games = 5
        try:
            for game_data in self.__playerData['last5Games']:
                goals += game_data['goals']
        except KeyError:
            return 0
            
        return goals/games
    
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
    
    def find_PPG(self):
        data = self.__teamData
        playerName = self.getName()
        for player in data["skaters"]:
            full_name = f"{player['firstName']['default']} {player['lastName']['default']}"
            if full_name.lower() == playerName.lower():
                return player['powerPlayGoals']
        return 0.0
    
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
            "{:s}".format(str(self.__bet)),
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
            "{:d}".format(self.__OTPM), stat_padding,
            "{:.2f}".format(self.__teamGoalsPerGame), stat_padding, 
            "{:.2f}".format(self.__otherTeamGoalsAgainst), stat_padding, 
            "{:d}".format(self.__isHome), stat_padding
        )
    
