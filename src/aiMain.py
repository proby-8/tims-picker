import os
import numpy as np
import time
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.layers import Input, Dense
from keras.models import Model

from Player import Player
import allPlayers
import saveData

def aiGuess():
    choice = 1
    if os.path.exists("randomModel"):
        choice = int(input("Would you like to use the saved AI model (0), or generate a new one (1): "))    
        if (choice != 0):
            verification = int(input("Are you sure you want to create a new model?\n(0) to cancel, (1) to create new: "))
            if (verification != 1):
                choice = 0

    startTime = time.time()
    experimentalTest(choice)
    print(f"Time elapsed: {(time.time() - startTime)}")


def experimentalTest(createNew, display=True):

    if (createNew):
        model = experimentalModel()

    # load the model
    model = tf.keras.models.load_model("randomModel")

    # get today's players
    players = allPlayers.getAllPlayers()

    playerInfo = saveData.oddsScraper.scraper() 

    saveData.linker(players, playerInfo)

    playersAI = []

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
        playerInfo = {
            'player': player,
            'predictVal': prediction
        }
        playersAI.append(playerInfo)

    
    # Sort the playersAI list based on 'predict' value in each dictionary
    sorted_playersAI = sorted(playersAI, key=lambda x: x['predictVal'], reverse=True)

    # Print the sorted list
    display = True
    if display:
        Player.printHeader()
    i=1
    for player_info in sorted_playersAI:
        player_info['player'].setStat(player_info['predictVal'])
        if display:
            print(f"{i}\t{player_info['player']}")
        i+=1

    return sorted_playersAI


def experimentalModel():
    # Load the data
    
    filename = "lib\\data.csv"
    try:
        data = pd.read_csv(filename, encoding="latin1")
    except UnicodeDecodeError:
        try:
            data = pd.read_csv(filename, encoding="utf-8")
        except UnicodeDecodeError:
            print("Manually save the csv file and try again.\n")
            exit(1)

    # Drop the rows where 'Scored' is empty
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
    model.save("randomModel")


if __name__ == "__main__":
    aiGuess()
    