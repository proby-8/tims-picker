import csv
import pandas as pd

def getCSVEncoding(filename):
    try:
        with open(filename, 'r', encoding='latin1') as file:
            _ = file.read()  # Try reading the file to detect encoding
        return 'latin1'
    except UnicodeDecodeError:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                _ = file.read()  # Try reading the file to detect encoding
            return 'utf-8'
        except UnicodeDecodeError:
            print("Manually save the csv file and try again.\n")
            exit(1)

def readCSV(filename):
    
    try:
        data = pd.read_csv(filename, encoding=getCSVEncoding(filename))
    except UnicodeDecodeError:
        print("Manually save the csv file and try again.\n")
        exit(1)
        
    return data

def findMatch(id, players):
    matching_player = None
    for player in players:
        if str(player['playerId']) == str(id):
            matching_player = player
            break  # Stop the loop once a match is found

    return matching_player

def updateGoalScorerRows(filename, date, playersWhoPlayed):

    try:
        with open(filename, 'r', endcoding=getCSVEncoding(filename)) as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header line
            rows = list(reader)  # Read the remaining rows into a list of lists    
    except UnicodeDecodeError:
        print("Manually save the csv file and try again.\n")
        exit(1)

    try:
        with open(filename, 'w', newline='', encoding=getCSVEncoding(filename)) as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write back the header line
            
            for row in rows:
                if row[0] == date:

                    # for each row in correct date
                    match = findMatch(row[3], playersWhoPlayed)

                    # if not match, remove from csv as they did not play
                    if match:
                        if (row[1] not in {0,1}):
                            # Check if player scored

                            if (match['goals'] > 0):
                                row[1] = '1'
                            else:
                                row[1] = '0'
                        writer.writerow(row)
                    
                else:
                    writer.writerow(row)
    except UnicodeDecodeError:
        print("Manually save the csv file and try again.\n")
        exit(1)
