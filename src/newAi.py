import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.layers import Input, Dense
from keras.models import Model
from Player import Player
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from Player import Player

def experimentalModel():
    # Load the data
    data = pd.read_csv('lib/data.csv')

    # Drop the rows where 'Scored' is empty
    statsToView = ['GPG','Last 5 GPG','HGPG','PPG','OTPM','TGPG','OTGA','Home (1)']
    statsToView = ['GPG', 'Last 5 GPG', 'OTGA']
    
    data = data[data['Scored'] != ' ']
    for col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Preprocess the data
    features = data[statsToView]
    # features = data[['GPG','Last 5 GPG','HGPG','PPG','OTPM','TGPG','OTGA','Home (1)']]
    labels = data['Scored']
    
    # Split the data into training and testing sets
    testSize = 0.2
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=testSize, random_state=42)
    
    # Normalize the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Define the input shape
    input_shape = (X_train.shape[1],)
    inputs = Input(shape=input_shape)

    # Define the layers
    x = Dense(64, activation='relu')(inputs)
    x = Dense(64, activation='relu')(x)
    outputs = Dense(1, activation='sigmoid')(x)

    # Create the model
    model = Model(inputs=inputs, outputs=outputs)

    # Compile the model with a specified learning rate
    model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))

    # Train the model
    model.fit(X_train, y_train, epochs=50, batch_size=32)

    # Evaluate the model
    loss = model.evaluate(X_test, y_test)

    print(f'Test loss: {loss}')

    # Save the model
    # model.save("randomModel")

    return model
    

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

    # train the df
    model = experimentalModel()
    # model = tf.keras.models.load_model("randomModel")

    # get all players
    players = []
    for index, normalized_row in normalized_features_df.iterrows():

        # Access label for the current row
        label = labels.loc[index]
        if label == ' ':

            players.append(Player(names[index], -1, -1, -1, -1, -1, -1, -1))
            
            players[-1].setId(ids[index])

            # players[-1].setStat(probability)
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

    # Assuming players is a list of player objects
    all_features = [list(player.getFeatures().values()) for player in players]
    all_features = np.array(all_features, dtype='float32')

    # Reshape for model input
    all_features_reshaped = all_features.reshape(len(players), -1)

    # Make predictions for all players at once
    probabilities = model.predict(all_features_reshaped, verbose=0)

    # Access individual predictions as needed
    for i, player in enumerate(players):
        prediction = probabilities[i][0]
        # Rest of your code
        player.setStat(prediction)
    
    return players

def get_stat(player):
    return player.getStat()

if __name__ == '__main__':
    players = getStats()
    sorted = sorted(players, key=get_stat, reverse=True)
    for p in sorted:
        print(p)

