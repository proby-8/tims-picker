import pandas as pd
import Player


def runTest():
    # init roster
    obj = Player.Player("")
    obj.initTeamsRosters()

    # init variables
    totalDays = 0
    totalCount = 0

    # read csv files into df
    dfs = [pd.read_csv("lib//train_test1.csv"),  pd.read_csv("lib//train_test2.csv"), pd.read_csv("lib//train_test3.csv")]
    for df in dfs:
        i=1
        count = 0
        days = 0
        while i < df.shape[0]:
            players = []
            scored = []
            # print(f"Date: {df['Date'][i-1]}")
            while ((i < df.shape[0]) and (df['Date'][i-1] == df['Date'][i])):
                players.append(Player.Player(df['Name'][i-1]))
                scored.append(df['Scored'][i-1])
                i+=1
            days += 1
            players.append(Player.Player(df['Name'][i-1]))
            scored.append(df['Scored'][i-1])
            i += 1

            # do work with array of players here
            highestStat = 0
            for x in range(0, len(players)):
                if (players[x].getStat() > players[highestStat].getStat()):
                    highestStat = x
            
            if (scored[highestStat]):
                count += 1
        
        print(f"Count: {count}")
        print(f"Count/Days: {count/days}")
        totalCount += count
        totalDays += days

    print(f"Total count: {totalCount}")
    print(F"Total Count/Total Days: {totalCount/totalDays}")