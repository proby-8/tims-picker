import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from keras.layers import Input, Dense
from keras.models import Model
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import newPlayer as Player
from newDataHandler import readCSV

statsToCheck = ['Bet', 'GPG', 'Last 5 GPG', 'HGPG', 'PPG', 'OTPM', 'OTGA']

def createModel( data ):
    # Drop the rows where 'Scored' is empty    
    data = data[data['Scored'] != ' ']
    for col in data.columns:
        data[col] = pd.to_numeric(data.loc[col], errors='coerce')

    # Preprocess the data
    features = data[statsToCheck]
    labels = data['Scored']
    
    X_train = features
    Y_train = labels
    
    # Normalize the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)

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
    model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001))

    # Train the model
    model.fit(X_train, Y_train, epochs=256, batch_size=64)

    # model.save("randomModel")

    return model


def main():

    # get data
    data = readCSV("lib/data.csv")

    # create model
    model = createModel(data)
    if model is None:
        print("Model creation failed. Exiting.")
        exit(1)

    # parse data
    features = data[['GPG', 'Last 5 GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home (1)']]
    usedFeatures = data[statsToCheck]
    labels = data['Scored']
    names = data['Name']
    teams = data['Team']
    bets = data['Bet']
    ids = data['ID']
    dates = data['Date']

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(usedFeatures)
    normalized_features_df = pd.DataFrame(normalized_features, columns=usedFeatures.columns)

    # Convert DataFrame directly to NumPy array
    all_features = normalized_features_df.to_numpy(dtype='float64')
    all_features_reshaped = all_features.reshape(len(features), -1)

    probabilities = model.predict(all_features_reshaped, verbose=0)

    players = []
    print(f"Making predictions for {dates.iloc[-1]}")
    for index, probability in enumerate(probabilities):

        label = labels.loc[index]
        if label == ' ':
            # Most recent day

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

def aiGuess():
    players = main()

    # sort by probability of scoring
    players = sorted(players, reverse=True)

    # print
    Player.Player.printHeader()
    for index, player in enumerate(players):
        print(f"{index+1}\t{player}")
        if index>450:
            break

def aiGuessNoPrint():
    players = main()
    return sorted(players, reverse=True)


if __name__ == "__main__":
    aiGuess()
