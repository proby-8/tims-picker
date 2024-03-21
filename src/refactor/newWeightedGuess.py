import datetime
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import newPlayer as Player
from newDataHandler import readCSV

def calculateStatNoComp(row, weights):
    
    if len(weights) != len(row):
        raise ValueError("Number of weights must match the number of features.")
    
    if round(sum(weights), 2) != 1:
        print(sum(weights))
        raise ValueError("Weights must add up to 1.")

    # Calculate the overallStat using the modified row
    overallStat = sum(w * stat for w, stat in zip(weights, row))
    return overallStat

def main():

    # get data
    data = readCSV("lib/data.csv")

    # parse data
    features = data[['GPG', 'Last 5 GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home (1)']]
    labels = data['Scored']
    names = data['Name']
    teams = data['Team']
    bets = data['Bet']
    ids = data['ID']
    dates = data['Date']

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(features)
    normalized_features_df = pd.DataFrame(normalized_features, columns=features.columns)

    # weights
    weights = [0.2, 0.3, 0.1, 0.1, 0.2, 0.0, 0.1, 0.0]

    players = []
    for index, normalized_row in normalized_features_df.iterrows():

        label = labels.loc[index]
        if label == ' ':
            # Most recent day

            # find probability
            probability = calculateStatNoComp(normalized_row, weights)

            if bets[index] > 0:
                bet = (f"+{bets[index]}")
            else:
                bet = (bets[index])

            players.append(Player.Player(names[index], 
                                         ids[index], 
                                         teams[index], 
                                         features['GPG'][index], 
                                         features['Last 5 GPG'][index], 
                                         features['HGPG'][index], 
                                         features['PPG'][index], 
                                         features['OTPM'][index], 
                                         features['TGPG'][index], 
                                         features['OTGA'][index], 
                                         features['Home (1)'][index], 
                                         bet, 
                                         probability))

    return players

def weightedGuess():
    players = main()

    # sort by probability of scoring
    players = sorted(players, reverse=True)

    # print
    Player.Player.printHeader()
    for index, player in enumerate(players):
        print(f"{index+1}\t{player}")

def weightedGuessNoPrint():
    
    # get data
    data = readCSV("lib/data.csv")

    # parse data
    features = data[['GPG', 'Last 5 GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home (1)']]
    labels = data['Scored']
    names = data['Name']
    teams = data['Team']
    bets = data['Bet']
    ids = data['ID']
    dates = data['Date']

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(features)
    normalized_features_df = pd.DataFrame(normalized_features, columns=features.columns)

    # weights
    weights = [0.2, 0.3, 0.1, 0.1, 0.2, 0.0, 0.1, 0.0]

    players = []
    probabilities = []
    for index, normalized_row in normalized_features_df.iterrows():

        label = labels.loc[index]
        if label == ' ':
            # Most recent day

            # find probability
            probability = calculateStatNoComp(normalized_row, weights)

            if bets[index] > 0:
                bet = (f"+{bets[index]}")
            else:
                bet = (bets[index])

            players.append(Player.Player(names[index], 
                                         ids[index], 
                                         teams[index], 
                                         features['GPG'][index], 
                                         features['Last 5 GPG'][index], 
                                         features['HGPG'][index], 
                                         features['PPG'][index], 
                                         features['OTPM'][index], 
                                         features['TGPG'][index], 
                                         features['OTGA'][index], 
                                         features['Home (1)'][index], 
                                         bet, 
                                         probability))
            probabilities.append(probability)
            
    # only take today's data
    # do this after calculating probability so data is normailzed over entire data set
    date = datetime.date.today().strftime('%Y-%m-%d')
    data = data[data['Date'] == date]

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
        
if __name__ == "__main__":
    weightedGuess()
