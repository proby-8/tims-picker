from guessMakerFunctions import getPlayerNames, getPlayerID, getGPGP, getGPGAT, getGPGFT, printTime
import datetime
import time

def main():

    start_time = time.time()
    date = datetime.date.today().strftime('%Y-%m-%d')
    groupsToLookAt=3

    # count number of rounds
    group = 1

    highestStats=[0,0,0]
    names= ["", "", ""]
    totalRounds=1
    roundStatsAverage = []

    eachRoundsGroups = []

    tempGroupNames = []
    tempGroupNames.append("")
    tempGroupNames.append("")
    tempGroupNames.append("")


    totalRounds=1
    while ((getPlayerNames(date+"/", totalRounds, group)) != (getPlayerNames(date+"/", totalRounds+1, group))):
        totalRounds+=1

    highestStats=[0,0,0]

    roundOfPicks=0
    while roundOfPicks<totalRounds:
        roundOfPicks+=1

        while group <= groupsToLookAt:
            print(f"Currently on round {roundOfPicks}, group {group}")

            players_fullName = (getPlayerNames(date+"/", roundOfPicks, group))

            x=0
            highest=0

            players_firstName = []
            players_lastName = []
            goalsPerGamePlayer = []
            gpgAgainstTeam = []

            stat = []

            for player in players_fullName:

                # this part getes players first and last name
                singePlayersFullname = player.split()
                players_firstName.append(singePlayersFullname[0])
                players_lastName.append(singePlayersFullname[1])

                # this gets a player's id number
                playerID = getPlayerID(players_firstName[x], players_lastName[x])

                # calculates a players goals per game
                goalsPerGamePlayer.append(getGPGP(playerID))

                # get goal average against a team
                gpgAgainstTeam.append(getGPGAT(playerID, date))

                # team gpg
                tgpg = getGPGFT(playerID)

                #create a value to measure
                stat.append(goalsPerGamePlayer[x]*tgpg)

                if stat[x] > stat[highest]:
                    highest = x
                
                x = x + 1

            # we now have the highest rated player for one group in one round
            highestStats[group-1] = stat[highest]
            names[group-1] = (players_firstName[highest] + " " + players_lastName[highest])
            tempGroupNames[group-1] = (players_firstName[highest] + " " + players_lastName[highest])

            group += 1


        # holds the overall average of each round to decide which round to use
        roundStatsAverage.append((highestStats[2] + highestStats[1] + highestStats[0]) / 3)
        eachRoundsGroups.append([tempGroupNames[0], tempGroupNames[1], tempGroupNames[2]])

        print(f"Best picks from round {roundOfPicks}: {[tempGroupNames[0], tempGroupNames[1], tempGroupNames[2]]}")

        tempGroupNames[0] = ""
        tempGroupNames[1] = ""
        tempGroupNames[2] = ""
        group = 1
        
    # choose best group
    highestAverage=0
    highestRoundNames=[]
    highestRound=0
    i=1 

    for average in roundStatsAverage:
        if average > highestAverage:
            highestRound=i
            highestAverage = average
            highestRoundNames = eachRoundsGroups[i-1]
        i+=1

    print(f"\nBest overall picks: (round {highestRound}):")
    print(f"{highestRoundNames[0]}\n{highestRoundNames[1]}\n{highestRoundNames[2]}\n")



    print("All done!")
    printTime(time.time() - start_time)
