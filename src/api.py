import csv
import datetime
import io
import json
from typing import Any, Dict, List
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import requests
from sklearn.preprocessing import MinMaxScaler
from Player import Player
from allPlayers import test
from oddsScraper import scraper
from saveData import linker
# import your_list_generator_script

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

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
    probabilities = []

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

            probabilities.append(probability)

    # only take today's data
    # do this after calculating probability so data is normailzed over entire data set
    data = data[data['Date'] == '2024-03-07']

    data.pop('Scored')
    data['Stat'] = probabilities
    data.rename(columns={'Home (1)': 'Home_1', 'Last 5 GPG': 'Last_5_GPG'}, inplace=True)
    data[['Date', 'Stat', 'Name', 'ID', 'Team', 'Bet', 'GPG', 'Last_5_GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home_1']] \
        = data[['Date', 'Stat', 'Name', 'ID', 'Team', 'Bet', 'GPG', 'Last_5_GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home_1']].astype(
            {'Date': str,
             'Stat': float,
             'Name': str,
             'ID': int,
             'Team': str,
             'Bet': str,
             'GPG': float,
             'Last_5_GPG': float,
             'HGPG': float,
             'PPG': float,
             'OTPM': float,
             'TGPG': float,
             'OTGA': float,
             'Home_1': int}
            )


    return data
        

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

def updateDatabase( data ):
    # Convert the CSV data to JSON
    # Convert DataFrame to dictionary
    data_dict = data.to_dict(orient='records')

    # Convert the dictionary to JSON
    json_data = json.dumps({"items": data_dict})

    json_data: Dict[str, List[Dict[str, Any]]] = json.loads(json_data)

    response = requests.patch("https://x8ki-letl-twmt.n7.xano.io/api:Cmz3Gtkc/addBulk", json=json_data)

    # Check the response
    if response.status_code == 200:
        print("Request was successful.")
        print("Response:", response.json())
    else:
        print("Request failed with status code:", response.status_code)
        print("Response:", response.text)


# @app.route('/api/list', methods=['GET'])
# def get_list():
#     return jsonify(jsonPlayers)

def main():
    import saveData
    saveData.main()
    data = getStats()
    updateDatabase(data)

if __name__ == '__main__':

    # Update data.csv
    import saveData
    saveData.main()

    # update database
    data = getStats()
    updateDatabase(data)

    # app.run(debug=True)

