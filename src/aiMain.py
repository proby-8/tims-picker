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

    startTime = time.time()
    test(choice)
    print(f"Time elapsed: {(time.time() - startTime)}")


def createNewModel():
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


def test(createNew):

    if (createNew):
        createNewModel()

    # load the model
    model = tf.keras.models.load_model("savedAiModel")

    # get today's players
    players = allPlayers.getAllPlayers()

    playersAI = []

    # Assuming players is a list of player objects
    all_features = [list(player.getFeatures().values()) for player in players]
    all_features = np.array(all_features, dtype='float32')

    # Reshape for model input
    all_features_reshaped = all_features.reshape(len(players), -1)

    # Make predictions for all players at once
    predictions = model.predict(all_features_reshaped, verbose=0)

    # Access individual predictions as needed
    for i, player in enumerate(players):
        prediction = predictions[i][0]
        # Rest of your code
        playerInfo = {
            'info': player,
            'predictVal': prediction
        }
        playersAI.append(playerInfo)
    
    # Sort the playersAI list based on 'predict' value in each dictionary
    sorted_playersAI = sorted(playersAI, key=lambda x: x['predictVal'], reverse=True)

    # Print the sorted list
    print("\nPlayers in order:")
    name_padding = 30
    stat_padding = 10
    print ("\t{:<{}} {:>{}} {:>{}} {:>{}} {:>{}}".format("Player Name", name_padding, "Stat", stat_padding, "GPG", stat_padding, "TGPG", stat_padding, "OTGA", stat_padding))   
    print("") 
    for player_info in sorted_playersAI:
        print(f"\t{stringFormat(player_info)}")

def stringFormat(player_info):
    name_padding = 30
    stat_padding = 10
    return "{:<{}} {:>{}} {:>{}} {:>{}} {:>{}}".format(player_info['info'].getName(), name_padding, "{:.2f}".format(player_info['predictVal']), stat_padding, "{:.2f}".format(player_info['info'].getGPG()), stat_padding, "{:.2f}".format(player_info['info'].getTGPG()), stat_padding, "{:.2f}".format(player_info['info'].getOTGA()), stat_padding)
