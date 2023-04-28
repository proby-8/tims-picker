import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

def make_input_fn(data_df, label_df, num_epochs=25, shuffle=False, batch_size=16):
    def input_function():  # inner function, this will be returned
        ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))  # create tf.data.Dataset object with data and its label
        if shuffle:
            ds = ds.shuffle(1000)  # randomize order of data
        ds = ds.batch(batch_size).repeat(num_epochs)  # split dataset into batches of 32 and repeat process for number of epochs
        return ds  # return a batch of the dataset
    return input_function  # return a function object for use

def main(df, group):

    dftrain = pd.read_csv(f"lib\\train_test{group+1}.csv")

    y_train = dftrain.pop('Scored')

    y_eval = []
    for i in range(0,df.shape[0]):
        y_eval.append(1)

    NUMERIC_COLUMNS = ["Goals per Game", "Team's Goals per Game", "Other Team's Goals Against"] #numeric categories
    CATEGORICAL_COLUMNS = ['Name']

    feature_columns = []
    for feature_name in CATEGORICAL_COLUMNS:
        vocabulary = dftrain[feature_name].unique()
        feature_columns.append(tf.feature_column.categorical_column_with_vocabulary_list(feature_name, vocabulary)) # stores feature names with their associated possibilities

    for feature_name in NUMERIC_COLUMNS:
        feature_columns.append(tf.feature_column.numeric_column(feature_name, dtype=tf.float32)) # stores columns with their possibilities

    train_input_fn = make_input_fn(dftrain, y_train, 1, False)

    eval_input_fn = make_input_fn(df, y_eval, 1, False)
    linear_est = tf.estimator.LinearClassifier(feature_columns=feature_columns)
    linear_est.train(train_input_fn)  # train

    linear_est.evaluate(eval_input_fn)  # get model metrics/stats by testing on testing data

    pred_dicts = list(linear_est.predict(eval_input_fn)) # all predicition info
    probs = pd.Series([pred['probabilities'][1] for pred in pred_dicts]) # probability of surviving

    # find highest prob
    highestProb = probs[0]
    highestIndex = 0
    for i in range(0,len(probs)):
        if probs[i] > highestProb:
            highestProb = probs[i]
            highestIndex = i

    return highestIndex

