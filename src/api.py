import csv
import datetime
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from Player import Player
from allPlayers import test
from oddsScraper import scraper
from saveData import linker
# import your_list_generator_script

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

jsonPlayers = None

def calculateStatNoComp(row, weights):
    
    if len(weights) != len(row):
        raise ValueError("Number of weights must match the number of features.")
    
    if round(sum(weights), 2) != 1:
        print(sum(weights))
        raise ValueError("Weights must add up to 1.")

    # Calculate the overallStat using the modified row
    overallStat = sum(w * stat for w, stat in zip(weights, row))
    return overallStat

def getStats():

    try:
        data = pd.read_csv('lib/data.csv')
    except UnicodeDecodeError:
        print("Manually save the csv file and try again.\n")
        exit(1)

    features = data[['GPG', 'Last 5 GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home (1)']]
    labels = data['Scored']
    names = data['Name']
    teams = data['Team']
    bets = data['Bet']
    ids = data['ID']

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(features)

    # The normalized_features is now a numpy array, you can convert it back to a DataFrame if needed
    normalized_features_df = pd.DataFrame(normalized_features, columns=features.columns)

    # Normalized weights
    weights = [0.2, 0.3, 0.1, 0.1, 0.2, 0.0, 0.1, 0.0]

    # weights = empiricalTest()
    players = []

    for index, normalized_row in normalized_features_df.iterrows():

        # Access label for the current row
        label = labels.loc[index]
        if label == ' ':

            # Your further logic with the normalized features and label
            probability = calculateStatNoComp(normalized_row, weights)
            players.append(Player(names[index], -1, -1, -1, -1, -1, -1, -1))
            
            players[-1].setId(ids[index])

            players[-1].setStat(probability)
            players[-1].setGPG(features['GPG'][index])
            players[-1].setTeamName(teams[index])
            if bets[index] > 0:
                players[-1].setBet(f"+{bets[index]}")
            else:
                players[-1].setBet(bets[index])
            players[-1].set5GPG(features['Last 5 GPG'][index])
            players[-1].setHGPG(features['HGPG'][index])
            players[-1].setPPG(features['PPG'][index])
            players[-1].setOTPM(features['OTPM'][index])
            players[-1].setTGPG(features['TGPG'][index])
            players[-1].setOTGA(features['OTGA'][index])
            players[-1].setHome(features['Home (1)'][index])

    jsonPlayers = []
    for p in players:
        jsonPlayers.append(p.toJSON())

    csvPlayers = []
    for p in players:
        csvPlayers.append(p.toCSV())

    currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
    with open('lib/export.csv', 'w', encoding='utf-8', newline='') as fd:
        fd.write(headerToCSV())  # Write back the header line
        for player in players:
            fd.write(f"{currentDate},")
            fd.write(toCSV(player))


    return jsonPlayers

def toCSV(self):
    csv_format = "{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
        self.getStat(),
        self.getName(),
        self.getId(),
        self.getTeamName(),
        "{:s}".format(str(self.getBet())),
        "{:f}".format(self.getGPG()),
        "{:f}".format(self.get5GPG()),
        "{:f}".format(self.getHGPG()),
        "{:f}".format(self.getPPG()),
        "{:d}".format(self.getOTPM()),
        "{:f}".format(self.getTGPG()),
        "{:f}".format(self.getOTGA()),
        "{:d}".format(self.isHome())
    )
    return csv_format+"\n"

def headerToCSV():
    csv_format = "{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
        "Date",
        "Stat",
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

@app.route('/api/list', methods=['GET'])
def get_list():
    return jsonify(jsonPlayers)

if __name__ == '__main__':
    jsonPlayers = getStats()
    # app.run(debug=True)

