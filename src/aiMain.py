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
import requests
import tensorflow as tf
import allPlayers

def aiGuess():
    choice = 1
    if os.path.exists("savedAiModel"):
        choice = int(input("Would you like to use the saved AI model (0), or generate a new one (1): "))
    
    if (choice != 0):
        verification = int(input("Are you sure you want to create a new model?\n(0) to use saved, (1) to create new: "))
        if (verification != 1):
            choice = 0
    test(choice)


def test(createNew):

    if (createNew):
        dataset1 = pd.read_csv("lib\\train_test1.csv")
        dataset2 = pd.read_csv("lib\\train_test2.csv")
        dataset3 = pd.read_csv("lib\\train_test3.csv")

        dataset = pd.concat([dataset1, dataset2, dataset3], ignore_index=True)

        # Separate features and labels
        labels = dataset.pop("Scored")
        dates = dataset.pop("Date")
        names = dataset.pop("Name")
        features = dataset

        # Split the data into training and testing sets
        totalDates = dates.unique()

        train_size = totalDates.size

        train_features = np.asarray(features).astype('float32')
        train_labels = labels

        # Create TensorFlow datasets
        train_dataset = tf.data.Dataset.from_tensor_slices((train_features, train_labels)).batch(1)

        # Define and compile the model
        model = tf.keras.models.Sequential([tf.keras.layers.Dense(1)])
        optimizer = tf.keras.optimizers.Adagrad(learning_rate=0.05)

        model.compile(optimizer=optimizer, loss="mse", metrics=['mae'])

        # Train the model
        numEpochs = int(input("Enter number of epochs: "))
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3, restore_best_weights=True)
        model.fit(train_dataset, epochs=numEpochs, callbacks=[early_stopping])

        model.fit(train_dataset, epochs=numEpochs)  # Adjust the number of epochs as needed

        # save the model
        model.save("savedAiModel")

    # load the model
    model = tf.keras.models.load_model("savedAiModel")


    # get today's players
    players = allPlayers.getAllPlayers()

    playersAI = []

    for player in players:        
        player_features = player.getFeatures()
        prediction_features = np.array(list(player_features.values())).astype('float32')
        prediction_features = prediction_features.reshape(1, -1)  # Reshape for model input
        prediction = model.predict(prediction_features, verbose=0)[0][0]

        playerInfo = {
            'info': player,
            'predictVal': prediction
        }
        playersAI.append(playerInfo)
    
    # Sort the playersAI list based on 'predict' value in each dictionary
    sorted_playersAI = sorted(playersAI, key=lambda x: x['predictVal'], reverse=True)

    # Print the sorted list
    print("\nPlayers in order:")

    for player_info in sorted_playersAI:
        print(f"\t{stringFormat(player_info)}")

def stringFormat(player_info):
    name_padding = 30
    stat_padding = 10
    return "{:<{}} {:>{}}".format(player_info['info'].getName(), name_padding, "{:.2f}".format(player_info['predictVal']), stat_padding)