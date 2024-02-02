import numpy as np
import pandas as pd
import tensorflow as tf


def test2(group, numEpoch):

    dataset = pd.read_csv(f"lib\\train_test{group}.csv")

    # Separate features and labels
    labels = dataset.pop("Scored")
    dates = dataset.pop("Date")
    names = dataset.pop("Name")
    features = dataset

    # Split the data into training and testing sets
    totalDates = dates.unique()
    train_dates_size = int(0.75 * totalDates.size)
    train_size = 0
    while (dates[train_size] != totalDates[train_dates_size]):
        train_size+=1

    train_features, test_features = np.asarray(features[:train_size]).astype('float32'), np.asarray(features[train_size:]).astype('float32')
    train_labels, test_labels = labels[:train_size], labels[train_size:]

    train_dates = dates[:train_size]
    test_dates = dates[train_size:]

    train_names = names[:train_size]
    test_names = names[train_size:]

    # Create TensorFlow datasets
    train_dataset = tf.data.Dataset.from_tensor_slices((train_features, train_labels)).batch(1)
    eval_dataset = tf.data.Dataset.from_tensor_slices((test_features, test_labels)).batch(1)

    # Define and compile the model
    model = tf.keras.models.Sequential([tf.keras.layers.Dense(1)])
    optimizer = tf.keras.optimizers.Adagrad(learning_rate=0.05)

    model.compile(optimizer=optimizer, loss="mse", metrics=['mae'])

    # Train the model
    model.fit(train_dataset, epochs=numEpoch)  # Adjust the number of epochs as needed

    # Get individual predictions
    predictions = model.predict(eval_dataset)

    # Make picks
    i = 0
    correct = 0
    while i < len(predictions):
        highestProbIndex = i

        while ((i != len(predictions) - 1) and (test_dates[train_size+i] == test_dates[train_size+i+1])):
            # print(f"Date: {test_dates[train_size+i]}, Name: {test_names[train_size+i]} : {predictions[i]}, Scored: {test_labels[train_size+i]}")
            if (predictions[i] > predictions[highestProbIndex]):
                highestProbIndex = i
            i+=1

        # get last guy
        # print(f"Date: {test_dates[train_size+i]}, Name: {test_names[train_size+i]} : {predictions[i]}, Scored: {test_labels[train_size+i]}")
        if (predictions[i] > predictions[highestProbIndex]):
            highestProbIndex = i
        
        # print(f"-----------------------------------------------------------------------------------")
        # print(f"Date: {test_dates[train_size+highestProbIndex]}")
        # print(f"Pick: {test_names[train_size+highestProbIndex]}, {predictions[highestProbIndex]}")
        # print(f"Pick scored value: " + str(test_labels[train_size+highestProbIndex]))
        if (test_labels[train_size+highestProbIndex]):
            correct += 1

        i+=1

    print(f"\n-----------------------------------------------------------------------------------")
    print(f"Total dates: {test_dates.unique().size}")
    print(f"Total correct: {correct}")
    print(f"Ratio: {correct / test_dates.unique().size}")

    return correct
