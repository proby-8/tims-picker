import datetime
import Player


def getPlayerNames(date, round, group): 

    return {"Mitchell Marner", "Auston Matthews", "Jack Hughes"}
    URL = "http://www.hockeychallengepicks.ca/history/" + date + str(round)

    try:
        '''
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="pick-" + str(group))
        '''
        results = BeautifulSoup(requests.get(URL).content, "html.parser").find(id="pick-" + str(group))
    except:
        print("Fatal error: Could not connect to source of player names.")
        exit(1)

    player = results.find_all("tr")
    players_fullName = [str(p.find("a"))[114:-4] for p in player]

    '''
    players_fullName = []
    x=0
    player = results.find_all("tr")
    for p in player:
        p = p.find("a")
        p = (str) (p)
        p = p[114:-4]

        players_fullName.append(p)
        x = x + 1
    '''
    return players_fullName


def getStats(curRound, group, date):
    # get player names
    players_fullName = (getPlayerNames(date+"/", curRound, group))

    allPlayers = []
    for name in players_fullName:
        player = Player.Player(name)

        # append dictionary to the list
        allPlayers.append(player)

    highestPlayer = allPlayers[0]
    for p in allPlayers:
        if (p.getStat() > highestPlayer.getStat()):
            highestPlayer = p

    return highestPlayer


def makeGuess():

    # get date
    date = datetime.date.today().strftime('%Y-%m-%d')
    groupsToLookAt=3

    # count number of rounds
    # totalRounds = getTotalRounds(date)
    totalRounds = 2
    print(f"Total of {totalRounds} rounds to check.\n")

    # init all stats
    highestStats=[0,0,0]
    roundStatsAverage = []
    eachRoundsGroups = []
    highestStats=[0,0,0]

    curRound=0

    # loop through each round
    while curRound<totalRounds:
        curRound+=1
        group=1

        # loop through each group
        while group <= groupsToLookAt:
            print(f"Currently on round {curRound}, group {group}")
            
            highestPlayer = getStats(curRound, group, date)

            # we now have the highest rated player for one group in one round
            highestStats[group-1] = highestPlayer

            group += 1


        # holds the overall average of each round to decide which round to use
        roundStatsAverage.append((highestStats[2].getStat() + highestStats[1].getStat() + highestStats[0].getStat()) / 3)
        eachRoundsGroups.append((highestStats[2].getName(), highestStats[1].getName(), highestStats[0].getName()))

        print(f"Best picks from round {curRound}: {eachRoundsGroups[-1]}\n")

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

    print(f"Best overall picks: (round {highestRound}):")
    print(f"{highestRoundNames[0]}\n{highestRoundNames[1]}\n{highestRoundNames[2]}\n")

