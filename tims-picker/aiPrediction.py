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
    group -= 1

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

    result = linear_est.evaluate(eval_input_fn)  # get model metrics/stats by testing on testing data

    pred_dicts = list(linear_est.predict(eval_input_fn)) # all predicition info
    probs = pd.Series([pred['probabilities'][1] for pred in pred_dicts]) # probability of surviving
    print(probs)
    print(result)


def useless():
        

    totalCorrect = 0
    totalWrong = 0

    # label_df = label data frame, y_train or y_eval in this case
    # num_epochs = the number of times the function goes through the dataset (too many and it will memorize test values, too few it will suck)
    # shuffle = shuffle the dataset
    # batch_size = the number of coloums or cases being made in the database


    print()

    dftrainAll = [None]*3
    dftrainAll[0] = pd.read_csv("lib\\train_test1.csv")
    dftrainAll[1] = pd.read_csv("lib\\train_test2.csv")
    dftrainAll[2] = pd.read_csv("lib\\train_test3.csv")

    y_train = []
    for df in dftrainAll:
        y_train.append(df.pop('Scored'))

    NUMERIC_COLUMNS = ["Goals per Game", "Team's Goals per Game", "Other Team's Goals Against"] #numeric categories
    CATEGORICAL_COLUMNS = ['Name']

    trainingGroup = 1
    train_input_fn = make_input_fn(dftrainAll[trainingGroup], y_train[trainingGroup], 1, False)

    i=-1
    for dftrain in dftrainAll:
        i+=1
        feature_columns = []
        for feature_name in CATEGORICAL_COLUMNS:
            vocabulary = dftrain[feature_name].unique()
            feature_columns.append(tf.feature_column.categorical_column_with_vocabulary_list(feature_name, vocabulary)) # stores feature names with their associated possibilities

        for feature_name in NUMERIC_COLUMNS:
            feature_columns.append(tf.feature_column.numeric_column(feature_name, dtype=tf.float32)) # stores columns with their possibilities

        print()
        print()
        # pd.concat([dftrain, y_train[i]], axis=1).groupby("Other Team's Goals Against").Scored.mean().plot(kind='line').set_xlabel("Percent chance they score")
        # plt.show()

        train_input_fn = make_input_fn(dftrainAll[i], y_train[i], 1, False)


        eval_input_fn = make_input_fn(dftrain, y_train[i], 1, False)
        linear_est = tf.estimator.LinearClassifier(feature_columns=feature_columns)
        linear_est.train(train_input_fn)  # train

        result = linear_est.evaluate(eval_input_fn)  # get model metrics/stats by testing on testing data

        pred_dicts = list(linear_est.predict(eval_input_fn)) # all predicition info
        probs = pd.Series([pred['probabilities'][1] for pred in pred_dicts]) # probability of surviving

        x=0
        highest=0
        correct=0
        wrong=0

        guesses = []
        dates = []

        oldDate = dftrain.loc[x]['Date']
        while (x < probs.shape[0]):
            newDate = dftrain.loc[x]['Date']
            # print("Old date: " + oldDate)
            if oldDate == newDate:
                # print("Info: ")
                # print(dfeval.loc[x]['Date'])
                # print("Probability we think they scored: ")
                # print(probs[x] * 100) # * 100 for percentage
                # print("Did they score: ")
                # print(y_eval.loc[x])

                # making guesses
                # print(probs[x])
                if (probs[x] >= probs[highest]):
                    highest = x
            else:
                # print(dfeval.loc[highest]['Name'])
                # print(dfeval.loc[highest]['Date'])
                guesses.append(dftrain.loc[highest]['Name'])
                dates.append(dftrain.loc[highest]['Date'])
                if 1 == y_train[i].loc[highest]:
                    correct+=1
                else:
                    wrong += 1

                oldDate = newDate
                highest=0
            x=x+1

        guesses.append(dftrain.loc[highest]['Name'])
        dates.append(dftrain.loc[highest]['Date'])
        if 1 == y_train[i].loc[highest]:
            correct+=1
        else:
            wrong += 1

        print("Correct: ")
        print(correct)
        print("Wrong: ")
        print(wrong)
        print("Overall: ")
        print(correct/(correct+wrong) * 100)
        totalCorrect += correct
        totalWrong += wrong


    print("\n\nAll done\n")
    print(totalCorrect)
    print(totalWrong)

    print(f"Overall average: {totalCorrect/totalWrong*100}")

