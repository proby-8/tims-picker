# stats
# - goals per game
# - other teams goals against
# - minutes played
# - possible stuff
#   - powerplay minutes
#   - (could look at other teams penalty minutes)

import os
import numpy as np
import pandas as pd
import time
from sklearn.discriminant_analysis import StandardScaler
import tensorflow as tf
from Player import Player
import allPlayers
import saveData

def aiGuess():
    choice = 1
    if os.path.exists("savedAiModel"):
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
        experimentalModel()

    # load the model
    model = tf.keras.models.load_model("savedAiModel")

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
    dataset = pd.read_csv("lib\\data.csv")

    # Filter out rows with non-numeric or empty values in the 'Scored' column
    dataset = dataset[pd.to_numeric(dataset['Scored'], errors='coerce').notna()]

    # Convert 'Scored' column to numeric
    dataset['Scored'] = pd.to_numeric(dataset['Scored'], errors='coerce')

    # Drop rows with NaN values
    dataset = dataset.dropna(subset=['Scored'])

    # Separate features and labels
    labels = dataset.pop("Scored")
    dates = dataset.pop("Date")
    names = dataset.pop("Name")
    try:
        dataset.pop("ID")
        dataset.pop("Team")
        # dataset.pop("Bet")
        # dataset.pop("Last 5 GPG")
        # dataset.pop("HGPG")
        # dataset.pop("PPG")
        # dataset.pop("OTPM")
        # dataset.pop("Home (1)")
    except Exception:
        print("Failed to pop data")
        pass

    features = dataset

    # Split the data into training and testing sets
    totalDates = dates.unique()

    train_size = totalDates.size

    train_features = np.asarray(features).astype('float32')
    train_labels = labels.values.astype('float32')

    # Create TensorFlow datasets
    from sklearn.utils import class_weight
    class_weights = class_weight.compute_sample_weight('balanced', train_labels)

    train_dataset = tf.data.Dataset.from_tensor_slices((train_features, train_labels, class_weights)).batch(1)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    optimizer = tf.keras.optimizers.Adagrad(learning_rate=0.05)

    model.compile(optimizer=optimizer, loss=tf.keras.losses.BinaryCrossentropy(), metrics=['accuracy'])
    # Train the model
    numEpochs = int(input("Enter number of epochs: "))

    model.fit(train_dataset, epochs=numEpochs)

    # save the model
    model.save("savedAiModel")