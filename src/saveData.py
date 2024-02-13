import allPlayers

def save():
    players = allPlayers.getAllPlayers()

    with open('lib/newlib.csv','a') as fd:
        for player in players:
            fd.write(player.toCSV())
